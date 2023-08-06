import logging
import threading
import time
import warnings
from typing import Dict, Union
from uuid import uuid4

from pydantic import BaseModel

from openmodule.config import settings
from openmodule.core import OpenModuleCore, core
from openmodule.dispatcher import MessageDispatcher
from openmodule.messaging import wait_for_connection
from openmodule.models.rpc import RPCResponse, RPCRequest, RPCResult
from openmodule.rpc.common import channel_to_response_topic, channel_to_request_topic


class RPCClient:
    class RPCEntry:
        def __init__(self, timeout):
            self.timestamp = time.time()
            self.timeout = timeout
            self.response = None
            self.ready = threading.Event()

        def done(self):
            return bool(self.response)

        def result(self, timeout=None):
            if (timeout) and (timeout > self.timeout):
                warnings.warn("You cannot extend the timeout of an RPC after sending the request. "
                              "The timeout will be limited to at most the initial timeout.", stacklevel=2)
                timeout = max(timeout, self.timeout)

            if self.response:
                return self.response
            else:
                timeout = timeout or self.timeout
                maximum_wait_time = (self.timestamp + timeout) - time.time()

                if maximum_wait_time < 0:  # timeout has already passed
                    raise TimeoutError()

                if not self.ready.wait(timeout=maximum_wait_time):
                    raise TimeoutError()

                assert self.response is not None, "internal error, this must not happen"
                return self.response

    def __init__(self, dispatcher: Union[OpenModuleCore, MessageDispatcher], channels=None, default_timeout=3.,
                 _warn=True):
        # TODO: backwards compatibiltiy, remove in next major version
        if isinstance(dispatcher, OpenModuleCore):
            warnings.warn(
                '\n\npassing an `OpenModuleCore` instance to the RPC Client is deprecated. Please migrate to '
                'passing a `MessageDispatcher` instead.\n',
                DeprecationWarning, stacklevel=2
            )
            dispatcher = dispatcher.messages
        # backwards compatibiltiy

        # the new design with one dedicated thread for the rpc client in the core discourages instantiating the
        # rpc client on its own. so we warn every user about this
        if _warn:
            warnings.warn(
                "\n\nInstantiating the RPC Client on your own is discouraged. PLease use the open module core's rpc "
                "client. For testcases or if you absolutely MUST for whatever reason instantiate the client pass "
                "`_warn=False` to the constructor.", DeprecationWarning, stacklevel=2
            )

        if channels is None:
            channels = []

        self.dispatcher = dispatcher
        self.log = logging.getLogger("rcp-client")
        self.lock = threading.Lock()
        self.results = dict()
        self.default_timeout = default_timeout
        self.running = True

        self.channels = []
        for channel in channels:
            self.register_channel(channel)
        if self.channels:
            wait_for_connection(self.dispatcher)

    def register_channel(self, channel):
        assert self.running, "Cannot register channels when rpc client is shutdown"
        if channel not in self.channels:
            self.channels.append(channel)
            topic = channel_to_response_topic(channel)
            self.log.debug("Registering channel: {}".format(topic))
            self.dispatcher.register_handler(topic, RPCResponse, self.receive, match_type=False)

    def unregister_channel(self, channel):
        self.channels.remove(channel)
        topic = channel_to_response_topic(channel)
        self.log.debug("Unregistering channel: {}".format(topic))
        self.dispatcher.unsubscribe(topic)

    def cleanup_old_results(self):
        now = time.time()
        with self.lock:
            to_delete = []
            for rpc_id, entry in self.results.items():
                if now > entry.timestamp + entry.timeout:
                    to_delete.append(rpc_id)
            for rpc_id in to_delete:
                self.results.pop(rpc_id, None)

    def _call(self, channel: bytes, typ: str, request: Dict, timeout: float):
        rpc_id = str(uuid4())

        request = RPCRequest(rpc_id=rpc_id, name=settings.NAME, request=request, type=typ)
        topic = channel_to_request_topic(channel)
        entry = self.RPCEntry(timeout=timeout)
        self.results[rpc_id] = entry
        core().publish(topic=topic, message=request)
        return entry

    def rpc(self, channel: bytes, type: str, request: [Dict, BaseModel],
            timeout: float = None, blocking=True) -> Union[RPCResult, RPCEntry]:

        self.cleanup_old_results()
        if isinstance(request, dict):
            warnings.warn(
                '\n\nPassing dicts as RPC Requests is deprecated and will be removed. Please '
                'define your RPC in a model and pass a model instance.\n',
                DeprecationWarning, stacklevel=2
            )

        if timeout is None:
            timeout = self.default_timeout

        if channel not in self.channels:
            self.register_channel(channel)
            wait_for_connection(self.dispatcher)

        entry = self._call(channel, type, request, timeout)
        if blocking:
            return entry.result(timeout=timeout)
        else:
            return entry

    def shutdown(self):
        self.running = False
        for channel in self.channels:
            self.unregister_channel(channel)

    def receive(self, response: RPCResponse):
        """handler that receives, saves and cleans up rpc responses"""
        self.cleanup_old_results()
        with self.lock:
            rpc_id = str(response.rpc_id)
            entry = self.results.get(rpc_id)
            if entry:
                status = "ok"
                if isinstance(response.response, dict) and response.response.get("status"):
                    status = response.response["status"]
                entry.response = RPCResult(status=status, response=response.response, rpc_id=response.rpc_id)
                entry.ready.set()
