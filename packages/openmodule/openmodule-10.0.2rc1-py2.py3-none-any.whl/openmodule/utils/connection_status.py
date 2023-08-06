import logging

from openmodule.dispatcher import EventListener, MessageDispatcher
from openmodule.models.base import ZMQMessage


class ConnectionStatusMessage(ZMQMessage):
    connected: bool
    type: str = "connection_status"


class ConnectionStatusListener:
    on_connect: EventListener
    on_disconnect: EventListener
    connected: bool = True
    _first_message: bool = True

    def __init__(self, dispatcher: MessageDispatcher):
        self.log = logging.getLogger(self.__class__.__name__)
        self.on_connect = EventListener(log=self.log)
        self.on_disconnect = EventListener(log=self.log)
        dispatcher.register_handler(b"connection_status", ConnectionStatusMessage, self.process_connection_status)

    def process_connection_status(self, message: ConnectionStatusMessage):
        """
        Forwards the current connection status of the ogclient
        """
        new_connected = message.connected
        if new_connected != self.connected or self._first_message:
            self._first_message = False
            self.connected = new_connected
            if new_connected:
                self.on_connect()
            else:
                self.on_disconnect()
