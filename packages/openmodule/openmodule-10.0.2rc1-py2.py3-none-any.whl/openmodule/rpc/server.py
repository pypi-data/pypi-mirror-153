import logging
import threading
import warnings
from collections import namedtuple
from typing import Callable, Dict, Optional, Type, Union, TypeVar

import zmq
from pydantic import ValidationError, BaseModel
from pydantic.main import ROOT_KEY

from openmodule.config import settings
from openmodule.dispatcher import DummyExecutor
from openmodule.messaging import get_sub_socket, get_pub_socket, receive_message_from_socket
from openmodule.models.rpc import RPCResponse, RPCRequest
from openmodule.rpc.common import channel_to_request_topic, channel_to_response_topic
from openmodule.threading import get_thread_wrapper
from openmodule.utils.schema import Schema

CallbackEntry = namedtuple("CallbackEntry", ["timestamp", "result"])
HandlerEntry = namedtuple("HandlerEntry", ["request_class", "response_class", "handler"])


def gateway_filter(gate=None, direction=None):
    def _filter(request, message, handler):
        gateway = request.get("gateway")
        if not gateway:
            return False
        return (not gate or gate == gateway.get("gate")) and \
               (not direction or direction == gateway.get("direction"))

    return _filter


class Filter:
    def __init__(self, filter, channel, type):
        self.filter = filter
        self.channel = channel
        self.type = type

    def check(self, request, message, handler, channel):
        if (self.channel is None or channel == self.channel) and (self.type is None or self.type == message.type):
            if self.filter(request=request, message=message, handler=handler):
                return True
            return False
        # filter does not apply
        return None


RequestType = TypeVar("RequestType")
ResponseType = TypeVar("ResponseType")


class RPCServer(object):
    def __init__(self, context, config=None, *, filter_resource=True, executor=None):
        """
        :param: executor: The executor to use for scheduling messages. The executor is shutdown
                          if the RPC Server is shutdown
        """
        if config:
            warnings.warn(
                "\n\nThe RPC Server no longer requires the config, but takes the openmodule global config instead. "
                "Please remove the argument. Future versions will remove the argument and leat to an error",
                DeprecationWarning, stacklevel=2
            )

        config = config or settings
        self.name = config.NAME
        self.sub = get_sub_socket(context, config)
        self.pub = get_pub_socket(context, config)
        self.pub_lock = threading.Lock()
        self.handlers: Dict[tuple, HandlerEntry] = {}
        self.filters = []
        self.running = True
        self.log = logging.getLogger(self.__class__.__name__)
        self.thread = None
        self.resource = None
        self.executor = executor or DummyExecutor()
        # since zmq does prefix matching we keep a list of unique channel names here
        # so we do not log a warning "unknown handler" if our channel is a prefix of a different channel
        self.registered_channels = set()
        if filter_resource:
            if config.RESOURCE:
                self.resource = config.RESOURCE
            else:
                self.log.error(
                    "Resource filter is active, but no resource is available. All RPCs requests will be processed. "
                    "This is ok for debugging / testing containers, but must not happen in production."
                )

    def add_filter(self, filter: Callable[[], bool], channel=None, type=None):
        """
        :param filter: filter function with paramters reqeust, message, handler
        :param channel: specific channel to filter or all channels if None
        :param type: specific type to filter or all types if None
        """
        self.filters.append(Filter(filter=filter, channel=channel, type=type))

    def shutdown(self, timeout=10):
        self.running = False
        self.executor.shutdown(wait=True)
        if self.thread:
            self.thread.join(timeout=timeout)
        else:
            with self.pub_lock:
                self.pub.close()
            self.sub.close()

    def register_handler(self, channel: str, type: str,
                         request_class: Type[RequestType],
                         response_class: Type[ResponseType],
                         handler: Callable[[RequestType, BaseModel], Union[ResponseType, Dict, None]],
                         register_schema=True):
        """
        :param channel: rpc channel you want to subscribe to, patterns/wildcards are not supported
        :param type: the request type
        :param request_class: Class definition of the request
        :param response_class: Class definition of the response
        :param handler: request handler of the form (request:Instance of request_class, full_message) -> Instance of response_class
                        if the handler returns a dict which contains the key "status",
                        then the value of "status" will be used as the rpc response status.
                        There are no other reserved keys except "status".
        :param register_schema: register the schema and models of this rpc during testing to create an automatic doc
        """
        if (channel, type) in self.handlers:
            raise ValueError(f"handler for {channel}:{type} is already registered")

        self.log.debug("register handler {}:{} -> {}".format(channel, type, handler))
        self.sub.subscribe(channel_to_request_topic(channel.encode("ascii")))
        self.handlers[(channel, type)] = HandlerEntry(request_class, response_class, handler)
        self.registered_channels = set(x[0] for x in self.handlers.keys())
        if register_schema:
            Schema.save_rpc(channel, type, request_class, response_class, handler)

    def _channel_from_topic(self, topic: bytes) -> str:
        return topic.split(b"-", 2)[-1].decode("ascii")

    def should_process_message(self, request, message, handler, channel):
        if self.filters:
            result = True
            for filter in self.filters:
                ok = filter.check(request=request, message=message, handler=handler, channel=channel)
                if ok:
                    return True
                # filter applies and is not ok
                elif ok is False:
                    result = False
            return result
        return True

    def find_handler(self, channel: str, type: str) -> HandlerEntry:
        return self.handlers.get((channel, type))

    def run_as_thread(self):
        assert not self.thread, "cannot run the same rpc server multiple times as thread"
        self.thread = threading.Thread(target=get_thread_wrapper(self.run))
        self.thread.start()
        return self.thread

    def _response_to_dict(self, response):
        data = response.dict()
        if response.__custom_root_type__:
            data = data[ROOT_KEY]
        return data

    def process_rpc(self, channel, message: RPCRequest) -> Optional[Dict]:
        if self.resource and message.resource and self.resource != message.resource:
            self.log.debug("a rpc was not processed because the resource did not mach. "
                           "my resource: %s, resource specified in rpc: %s", self.resource, message.resource)
            return None

        if settings.LOG_LEVEL == logging.DEBUG:
            self.log.debug("received RPC channel: %s, type: %s, request: %s", channel, message.type, message.request)
        else:
            self.log.info("received RPC channel: %s, type: %s", channel, message.type)

        handler: HandlerEntry = self.find_handler(channel, message.type)
        if handler:
            try:
                request = handler.request_class(**message.request)
            except ValidationError as e:
                return {"status": "validation_error", "exception": e.json()}

            try:
                if not self.should_process_message(request, message, handler, channel):
                    return None
            except Exception as e:
                self.log.exception("exception in message filter. request not processed and error returned")
                return {"status": "filter_error", "exception": str(e)}

            try:
                response = handler.handler(request, message)
                if isinstance(response, handler.response_class):
                    # shortcut prevent serialization and de-serialization if the correct response
                    # is already returned
                    return self._response_to_dict(response)
                else:
                    response = handler.response_class.parse_obj(response or {})
                    return self._response_to_dict(response)
            except Exception as e:
                self.log.exception("exception in handler {}:{}".format(channel, message.type))
                return {"status": "handler_error", "exception": str(e)}
        else:
            self.log.warning("no handler found for {}:{}".format(channel, message.type))
            return None

    def _process_rpc_message(self, topic, message):
        try:
            channel = self._channel_from_topic(topic)

            # this filters prefix-matched topics from other channels early
            if channel not in self.registered_channels:
                return

            try:
                message = RPCRequest(**message)
                message_type = message.type
                rpc_id = message.rpc_id
            except ValidationError as e:
                message_type = "unknown"
                rpc_id = None
                response = {"status": "validation_error", "exception": e.json()}
            else:
                response = self.process_rpc(channel, message)

            if response is not None:
                self.log.debug("response: {}".format(response))
                if "status" not in response:
                    response["status"] = "ok"

                result = RPCResponse(
                    type=message_type,
                    rpc_id=rpc_id,
                    response=response,
                    name=self.name
                )
                with self.pub_lock:
                    result.publish_on_topic(
                        self.pub,
                        channel_to_response_topic(channel.encode("ascii")),
                    )
        except Exception:
            self.log.exception("Unknown exception while processing an rpc. No answer could was sent to the caller.")
        except zmq.ContextTerminated:
            self.log.warning(
                "context terminated while RPC request was being processed. The result might not have been sent."
            )

    def run(self):
        poller = zmq.Poller()
        poller.register(self.sub, zmq.POLLIN)
        try:
            while self.running:
                socks = dict(poller.poll(timeout=1000))
                if socks.get(self.sub) != zmq.POLLIN:
                    continue
                topic, message = receive_message_from_socket(self.sub)
                if topic is None:
                    continue
                if self.running:
                  # someone may have stopped our server while we were receiving a message
                  self.executor.submit(self._process_rpc_message, topic, message)
        except zmq.ContextTerminated:
            pass
        finally:
            self.sub.close()
            with self.pub_lock:
                self.pub.close()
