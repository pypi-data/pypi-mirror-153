import logging
from typing import List

from openmodule.core import OpenModuleCore
from openmodule.models.backend import AccessRequest, AccessResponse, CountMessage, MediumAccesses, Access, \
    BackendRegisterMessage, BackendRegisterRequestMessage, BackendUnregisterMessage, SessionStartMessage, \
    SessionFinishMessage
from openmodule.rpc.server import RPCServer


class Backend:
    """
    Backend template class
    provides basic functionality used for backups
    * subscribes to BackendMessages and automatically registers backend
    * subscribes to CountMessages and calls check_in/check_out correspondingly
    * provides method for the backend / auth rpc with the check_backend_access method

    """

    def __init__(self, core: OpenModuleCore, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.core = core
        self.log = logging.getLogger()

        self.register_at_controller()
        self.core.messages.register_handler(b"count", CountMessage, self.handle_message)
        self.core.messages.register_handler(b"backend", BackendRegisterRequestMessage,
                                            self.handle_backend_register_request)
        self.core.messages.register_handler(b"session", SessionStartMessage, self.handle_session_start_message)
        self.core.messages.register_handler(b"session", SessionFinishMessage, self.handle_session_finish_message)

    def register_rpcs(self, rpc_server: RPCServer):
        rpc_server.add_filter(self._backend_filter, "backend", "auth")
        rpc_server.register_handler("backend", "auth", request_class=AccessRequest,
                                    response_class=AccessResponse, handler=self.rpc_check_access)

    def _backend_filter(self, request, message, handler) -> bool:
        backend = request.name
        if not backend:
            return False
        return self.core.config.NAME == backend

    def check_access(self, request: AccessRequest) -> List[Access]:
        """
        this method checks if current mediums has access to parking lot
        it should raise an Exception if it fails
        :param request: AccessRequest
        :return: Acesses
        """
        raise NotImplementedError()

    def check_in(self, message: CountMessage):
        """
       this method should check in the user of the message in the backend
        it should raise an Exception if it fails
       :param message: CountMessage
       """
        raise NotImplementedError()

    def check_out(self, message: CountMessage):
        """
        this method should check out the user of the message of the backend
        :param message: CountMessage
        """
        raise NotImplementedError()

    def check_in_session(self, message: SessionStartMessage):
        """
       this method should check in the user of the message in the backend
        it should raise an Exception if it fails
       :param message: SessionStartMessage
       """
        raise NotImplementedError()

    def check_out_session(self, message: SessionFinishMessage):
        """
        this method should check out the user of the message of the backend
        :param message: SessionFinishMessage
        """
        raise NotImplementedError()

    def shutdown(self):
        self.unregister_at_controller()

    def handle_session_start_message(self, message: SessionStartMessage):
        """
        Checks the user in with the data of the session start message
        """
        self.log.debug(f"received a session check in message for user {message.user_id}")
        try:
            self.check_in_session(message)
        except Exception as e:
            self.log.exception(f"Error in session check in for user {message.user_id}", extra=message.dict())

    def handle_session_finish_message(self, message: SessionFinishMessage):
        """
        Checks the user out with the data of the session finish message
        """
        self.log.debug(f"received a session check out message for user {message.user_id}")
        try:
            self.check_out_session(message)
        except Exception as e:
            self.log.exception(f"Error in session check out for user {message.user_id}", extra=message.dict())

    def handle_message(self, message):
        """
        Checks the user in/out based on the received CountMessage
        """
        try:
            self.log.debug(f"received a check {message.gateway.direction} message for user {message.user}")
            if message.gateway.direction == "in":
                self.check_in(message)
            else:
                self.check_out(message)
            return True
        except Exception as e:
            self.log.exception(f"error in check_{message.gateway.direction} for user {message.user}")
            return False

    def rpc_check_access(self, request: AccessRequest, _) -> AccessResponse:
        """
        Check if the user has access at the given gate
        """
        gate_log_string = f"({request.gateway.gate}/{request.gateway.direction})" if request.gateway else ""

        try:
            accesses = self.check_access(request)
        except Exception as e:
            self.log.exception(f"check access request had an internal error {gate_log_string}")
            return AccessResponse(success=False,
                                  medium=MediumAccesses(accesses=[], id=request.medium_id, type=request.medium_type))

        if accesses:
            self.log.info(
                f"{request.medium_id}:{request.medium_type} has {len(accesses)} permissions {gate_log_string}"
            )
            return AccessResponse(
                success=True,
                medium=MediumAccesses(medium_id=request.medium_id, medium_type=request.medium_type, accesses=accesses)
            )
        else:
            self.log.info(
                f"{request.medium_id} medium {request.medium_type} has NO parking permissions {gate_log_string}"
            )
            return AccessResponse(success=True,
                                  medium=MediumAccesses(accesses=[], id=request.medium_id, type=request.medium_type))

    def handle_backend_register_request(self, _):
        """
        Registers the backend if the message type is register_request
        """
        self.register_at_controller()

    def register_at_controller(self):
        self.core.publish(BackendRegisterMessage(), b"backend")

    def unregister_at_controller(self):
        self.core.publish(BackendUnregisterMessage(), b"backend")
