import gzip
import json
import logging
import threading
import warnings
from collections import defaultdict
from concurrent.futures._base import Executor
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from typing import Union, Optional, Callable, DefaultDict, List, Dict, TypeVar, Type, Generic

import zmq
from pydantic import ValidationError, BaseModel

from openmodule.config import settings
from openmodule.models.base import ZMQMessage
from openmodule.utils.schema import Schema


class DummyExecutor(Executor):
    def __init__(self):
        self._shutdown = False
        self._shutdown_lock = threading.Lock()

    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')

            fn(*args, **kwargs)

    def shutdown(self, wait=True):
        if wait:
            with self._shutdown_lock:
                self._shutdown = True
        else:
            self._shutdown = True


class Listener:
    def __init__(self, message_class: Type[ZMQMessage], type: Optional[str], filter: Optional[Callable],
                 handler: Callable):
        self.filter = filter
        self.handler = handler
        self.type = type
        self.message_class = message_class

    def matches(self, message: Dict):
        if self.type and message.get("type") != self.type:
            return False

        if self.filter:
            return self.filter(message)
        else:
            return True


EventArgs = TypeVar("EventArgs")


class EventListener(Generic[EventArgs], list):
    """
    note: the generic may not work as intended, but it is nevertheless a nice way to document the event
    handler arguments
    """
    log: Optional[logging.Logger]

    def __init__(self, *args, log=None, raise_exceptions=False):
        super().__init__(args)
        self.raise_exceptions = raise_exceptions
        self.log = log or logging

    def __call__(self, *args: EventArgs):
        for f in self:
            try:
                f(*args)
            except zmq.ContextTerminated:
                raise
            except Exception as e:
                if self.raise_exceptions:
                    raise
                else:
                    self.log.exception(e)


ZMQMessageSub = TypeVar('ZMQMessageSub', bound=ZMQMessage)


class MessageDispatcher:
    def __init__(self, name=None, *, raise_validation_errors=False, raise_handler_errors=False,
                 executor: Optional[Executor] = None):
        """
        :param name: optionally name the dispatcher for logging purposes
        :param raise_validation_errors: if true and received messages do not match a validation error is raised,
                                        this is useful in restricive code or testcases
        :param raise_handler_errors: if true and a message handler raises an exception, the exception is raised,
                                     this is useful in restricive code or testcases
        """

        assert executor is None or not (raise_handler_errors or raise_validation_errors), (
            "raise errors is only supported if no executor is used."
        )

        self.name = name
        self.log = logging.getLogger(f"{self.__class__.__name__}({self.name})")
        self.listeners: DefaultDict[bytes, List[Listener]] = defaultdict(list)
        self.raise_validation_errors = raise_validation_errors
        self.raise_handler_errors = raise_handler_errors
        self.executor = executor or DummyExecutor()

    @property
    def is_multi_threaded(self):
        if isinstance(self.executor, DummyExecutor):
            return False

        if isinstance(self.executor, (ThreadPoolExecutor, ProcessPoolExecutor)):
            # noinspection PyProtectedMember
            if self.executor._max_workers > 1:
                return True
            else:
                return False

        # unknown executor? assume multithreaded
        return True

    def shutdown(self, wait=True):
        self.executor.shutdown(wait=wait)

    def unregister_handler(self, listener: Listener):
        for topic, listeners in self.listeners.items():
            try:
                listeners.remove(listener)
            except ValueError:
                pass

    def _is_test_handler(self, handler):
        """
        this breaks separation a bit by including test specific code in the main module
        but it improves developer usability drastically
        """
        if settings.TESTING and "Mock" in str(handler):
            return True
        else:
            return False

    def register_handler(self, topic: Union[bytes, str],
                         message_class: Type[ZMQMessageSub],
                         handler: Callable[[ZMQMessageSub], None], *,
                         filter: Optional[Union[Dict, Callable[[Dict], bool]]] = None,
                         match_type=True,
                         register_schema=True):
        """
        registers a message handler. without any filters all messages from the topic are
        sent to the message handler.
        :param filter: a dictionary of values which must match in order for the message to
                       be further processed
        :param match_type: if set to true the message_class's type field is used as a filter.
                           equivalent to setting filter={"type": message_class.fields["type"].default}
        """

        if hasattr(topic, "encode"):
            topic = topic.encode()

        # deprecation warning for old style filters
        if isinstance(filter, dict):
            warnings.warn(
                "\n\nDict-style filters are deprecated and will be removed in the next version. Please migrate to\n"
                "using function-style filters. For an equal filter (albeit maybe an ugly solution) you can\n"
                "use\n"
                f"  register_handler(..., filter=lambda msg: (msg.items() >= {filter}.items())\n"
                "\n"
                "If you were previously filtering for gate+direction you now HAVE TO re-write your filter to \n"
                "**only match the gate name** and **not the direction!**\n", stacklevel=3
            )
            filter_dict = filter
            filter = lambda msg: (msg.items() >= filter_dict.items())

        if match_type:
            assert "type" in message_class.__fields__ and message_class.__fields__["type"].default, (
                "\n\nYour message class definition does not set a `type` field, or the type field "
                "does not have a default value! To receive all message type pass `match_type=False` to "
                "`register_handler`. Otherwise please define a `type` for your message class."
            )
            type = message_class.__fields__["type"].default
        else:
            type = None

        listener = Listener(message_class, type, filter, handler)
        self.listeners[topic].append(listener)

        if register_schema and not self._is_test_handler(handler):
            Schema.save_message(topic, message_class, handler, filter)

        return listener

    def dispatch(self, topic: bytes, message: Union[Dict, BaseModel]):
        if isinstance(message, BaseModel):
            message = message.dict()

        listeners = self.listeners.get(topic, [])
        for listener in listeners:
            if listener.matches(message):
                self.executor.submit(self.execute, listener, message)

    def execute(self, listener: Listener, message: Dict):
        try:
            parsed_message = listener.message_class.parse_obj(message)
        except ValidationError as e:
            if self.raise_validation_errors:
                raise e from None
            else:
                self.log.exception("Invalid message received")
        else:
            try:
                listener.handler(parsed_message)
            except zmq.ContextTerminated:
                raise
            except Exception as e:
                if self.raise_handler_errors:
                    raise e from None
                else:
                    self.log.exception("Error in message handler")


class SubscribingMessageDispatcher(MessageDispatcher):
    def __init__(self, subscribe: Callable[[bytes], None], name=None, *, raise_validation_errors=False,
                 raise_handler_errors=False, unsubscribe: Optional[Callable[[bytes], None]] = None,
                 executor: Optional[Executor] = None):
        super().__init__(name=name, raise_validation_errors=raise_validation_errors,
                         raise_handler_errors=raise_handler_errors, executor=executor)
        self.subscribe = subscribe
        self.unsubscribe = unsubscribe

    def register_handler(self, topic: Union[bytes, str],
                         message_class: Type[ZMQMessageSub],
                         handler: Callable[[ZMQMessageSub], None], *,
                         filter: Optional[Dict] = None,
                         register_schema=True,
                         match_type=True):
        if topic and hasattr(topic, "encode"):
            topic = topic.encode()
        self.subscribe(topic)
        return super().register_handler(topic, message_class, handler, filter=filter,
                                        register_schema=register_schema, match_type=match_type)

    def unregister_handler(self, listener: Listener):
        super().unregister_handler(listener)

        warn_no_unsubscribe = False
        for topic, listeners in self.listeners.items():
            if not listeners:
                if self.unsubscribe:
                    self.unsubscribe(topic)
                else:
                    warn_no_unsubscribe = True
                    break

        if warn_no_unsubscribe:
            warnings.warn("All handlers were unregistered from a topic, but no unsubscribe method was configured. "
                          "This may cause a performance overhead if too many unused subscriptions are kept. "
                          "Consider passing a unsubscribe method.", UserWarning, stacklevel=2)


class ZMQMessageDispatcher(SubscribingMessageDispatcher):
    def __init__(self, sub_socket: zmq.Socket, name=None, *, raise_validation_errors=False, raise_handler_errors=False,
                 executor: Optional[Executor] = None):
        super().__init__(
            subscribe=lambda x: sub_socket.subscribe(x),
            unsubscribe=lambda x: sub_socket.unsubscribe(x),
            name=name,
            raise_validation_errors=raise_validation_errors,
            raise_handler_errors=raise_handler_errors,
            executor=executor
        )


class DeeplogMessageDispatcher(MessageDispatcher):
    def __init__(self, path: Union[Path, str], name=None, *, raise_validation_errors=False, raise_handler_errors=False,
                 executor: Optional[Executor] = None):
        super().__init__(name, raise_validation_errors=raise_validation_errors,
                         raise_handler_errors=raise_handler_errors, executor=executor)
        if not isinstance(path, Path):
            path = Path(path)

        assert path.is_dir()
        self.path = path
        self.current_timestamp = None

    def dispatch_hour(self, date_string):
        logging.info(f"Dispatching {date_string}")
        # prefer .gz files over .log since gz are finished
        gz_path = self.path / f"hour_{date_string}.log.gz"
        raw_path = self.path / f"hour_{date_string}.log"
        file_handle = None

        try:
            if gz_path.exists():
                file_handle = gzip.open(gz_path, "rb")

            elif raw_path.exists():
                file_handle = open(raw_path, "rb")

            else:
                raise FileNotFoundError(f"log file for hour {date_string} does not exist")

            try:
                for line in file_handle.readlines():
                    try:
                        topic, message = json.loads(line)
                    except:
                        logging.warning("broken message skipped")
                    else:
                        self.current_timestamp = message.get("timestamp")
                        self.dispatch(topic.encode(), message)
            except EOFError as e:
                logging.error(str(e))

        finally:
            if file_handle:
                file_handle.close()

    def dispatch_all(self):
        hours = []
        for file in self.path.iterdir():
            if file.is_file() and file.name.startswith("hour_"):
                date_string = file.name[5:].split(".")[0]
                hours.append(date_string)

        hours.sort()
        for hour in hours:
            self.dispatch_hour(hour)
