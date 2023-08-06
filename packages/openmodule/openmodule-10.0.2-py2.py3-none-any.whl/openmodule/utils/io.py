import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Union, Optional

import zmq

from openmodule.dispatcher import MessageDispatcher, Listener
from openmodule.models.base import Gateway
from openmodule.models.io import IoMessage, IoState


class IoListener:
    """
    The IoListener passes the IoState of any registered pin or gateway when the logical state of the pin/gateway
    changes (or doesn't change) as registered (edge_rising, edge_falling, edge_any, edge_none).
    The IoListener additionally save the current stage of ALL pins.
    """
    current_states: Dict[str, IoState] = defaultdict(IoState)
    listeners: List[Listener] = list()

    def __init__(self, dispatcher: MessageDispatcher, raise_handler_errors=False):
        assert not dispatcher.is_multi_threaded, (
            "you cannot use a multithreaded message dispatcher for the presence listener. It is highly reliant "
            "on receiving messages in the correct order!"
        )
        self.log = logging.getLogger(self.__class__.__name__)
        self.raise_handler_errors = raise_handler_errors
        dispatcher.register_handler(b"io", IoMessage, self._on_io_message, match_type=False)

    def add_listener_edge_rising(self, listen_to: Union[str, Gateway], callback: Callable[[IoState], None],
                                 io_type: Optional[str] = None):
        """
        Calls the given callback method whenever a message is received and the given pin or a pin of the given Gateway
        changes its value from 0 to 1 (rising edge)
        param listen_to: the pin or Gateway that needs to experience a rising edge to call the callback
        param callback: the function that is called when a rising edge occurs on listen_to
        param io_type: the io_type to filter for (input, output)
        """
        self._add_listener(edge="rising", listen_to=listen_to, callback=callback, io_type=io_type)

    def add_listener_edge_falling(self, listen_to: Union[str, Gateway], callback: Callable[[IoState], None],
                                  io_type: Optional[str] = None):
        """
        Calls the given callback method whenever a message is received and the given pin or a pin of the given Gateway
        changes its value from 1 to 0 (falling edge)
        param listen_to: the pin or Gateway that needs to experience a falling edge to call the callback
        param callback: the function that is called when a falling edge occurs on listen_to
        param io_type: the io_type to filter for (input, output)
        """
        self._add_listener(edge="falling", listen_to=listen_to, callback=callback, io_type=io_type)

    def add_listener_edge_any(self, listen_to: Union[str, Gateway], callback: Callable[[IoState], None],
                              io_type: Optional[str] = None):
        """
        Calls the given callback method whenever a message is received and the given pin or a pin of the given Gateway
        changes its value (either from 0 to 1 (rising edge) or from 1 to 0 (falling edge))
        param listen_to: the pin or Gateway that needs to experience an edge to call the callback
        param callback: the function that is called when an edge occurs on listen_to
        param io_type: the io_type to filter for (input, output)
        """
        self._add_listener(edge="any", listen_to=listen_to, callback=callback, io_type=io_type)

    def add_listener_edge_none(self, listen_to: Union[str, Gateway], callback: Callable[[IoState], None],
                               io_type: Optional[str] = None):
        """
        Calls the given callback method whenever a message is received and the given pin or a pin of the given Gateway
        doesn't change
        param listen_to: the pin or Gateway that is in the message
        param callback: the function that is called when a message with the given listen_to is received
        param io_type: the io_type to filter for (input, output)
        """
        self._add_listener(edge="none", listen_to=listen_to, callback=callback, io_type=io_type)

    def _add_listener(self, edge: str, listen_to: Union[str, Gateway], callback: Callable[[IoState], None],
                      io_type: Optional[str] = None):

        assert isinstance(listen_to, (str, Gateway))

        def message_filter(msg):
            if isinstance(listen_to, str):
                if msg.get("pin") != listen_to:
                    return False
            elif isinstance(listen_to, Gateway):
                if (msg.get("gateway") or {}).get("gate") != listen_to.gate:
                    return False

            filter_dict = {}
            if edge == "rising":
                filter_dict.update(value=1, edge=1)
            elif edge == "falling":
                filter_dict.update(value=0, edge=1)
            elif edge == "any":
                filter_dict.update(edge=1)
            elif edge == "none":
                filter_dict.update(edge=0)
            if io_type is not None:
                filter_dict.update(type=io_type)

            return msg.items() >= filter_dict.items()

        self.listeners.append(Listener(IoMessage, None, message_filter, callback))

    def is_pin_valid(self, pin: str, timeout: Optional[int] = 5) -> bool:
        """
        Returns true if the given pin is present in the saved IoStates and it has received a message in the last
        'timeout' seconds (default 5)
        """
        return pin in self.current_states and \
               self.current_states[pin].last_timestamp > datetime.utcnow() - timedelta(seconds=timeout)

    def get_pin_state(self, pin: str) -> IoState:
        """
        Returns the current IoState of the given pin, or a default IoState (all values 0) if the pin does not yet exist
        """
        return self.current_states.get(pin, IoState(pin="", gateway=Gateway(gate="", direction=""), type="", value=0,
                                                    physical=0, inverted=False,
                                                    last_timestamp=datetime.fromtimestamp(0)))

    def is_gateway_valid(self, gateway: Gateway, timeout: Optional[int] = 5) -> bool:
        """
        Returns true if the given Gateway is present in the saved IoStates and it has received a message in the last
        'timeout' seconds (default 5)
        """
        return any(gateway == x.gateway and x.last_timestamp > datetime.utcnow() - timedelta(seconds=timeout)
                   for x in self.current_states.values())

    def get_gateway_states(self, gateway: Gateway) -> List[IoState]:
        """
        Returns a list the current IoStates of the given Gateway, or a list with 1 default IoState (all values 0) if
        the Gateway does not yet exist
        """
        x = list(filter(lambda state: state.gateway == gateway, self.current_states.values()))
        return x if x else [IoState(pin="", gateway=Gateway(gate="", direction=""), type="", value=0, physical=0,
                                    inverted=False, last_timestamp=datetime.fromtimestamp(0))]

    def _on_io_message(self, message: IoMessage):
        """
        This handler receives all IO Messages, saves any changes and calls any listeners registered in the IoListener
        """
        if message.pin not in self.current_states:
            """
            No IO Message with this gate was received before.
            A new entry in the current_states dict needs to be created.
            """

            if "physical" not in message:
                message.physical = message.value if not message.inverted else 1 - message.value
            message.edge = 1
            self.current_states[message.pin] = IoState(pin=message.pin, gateway=message.gateway, type=message.type,
                                                       value=message.value, physical=message.physical,
                                                       inverted=message.inverted, last_timestamp=message.timestamp)

        elif (message.edge == 1) or (self.current_states[message.pin].value != message.value) or \
                (self.current_states[message.pin].inverted != message.inverted):
            """
            The state of this gate was changed, or edge is 1.
            The entry in the current_states dict needs to be updated.
            """
            if "physical" not in message:
                message.physical = message.value if not message.inverted else 1 - message.value
            message.edge = 1
            self.current_states[message.pin].value = message.value
            self.current_states[message.pin].physical = message.physical
            self.current_states[message.pin].inverted = message.inverted
            self.current_states[message.pin].last_timestamp = message.timestamp

        message = message.dict()
        for listener in self.listeners:
            """
            Handles the registered listeners the same as the dispatcher.
            Is copied here because all messages are needed to keep current_states up to date.            
            """
            if listener.matches(message):
                try:
                    listener.handler(self.current_states[message["pin"]])
                except zmq.ContextTerminated:
                    raise
                except Exception as e:
                    if self.raise_handler_errors:
                        raise e from None
                    else:
                        self.log.exception("Error in message handler")
