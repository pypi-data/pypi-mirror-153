import logging
import re

from openmodule.core import OpenModuleCore
from openmodule.models.validation import ValidationRegisterRequestMessage, ValidateResponse, ValidateRequest, \
    ValidationRegisterMessage, ValidationUnregisterMessage
from openmodule.rpc.server import RPCServer
from openmodule.utils.misc_functions import clean_service_name


class Validation:
    """
    Validation provider template class
    provides basic functionality used for validation providers
    * subscribes to ValidationMessages and automatically registers validation_provider
    * provides method for the validation_provider / validate rpc with the validate_ticket method
    """

    def __init__(self, core: OpenModuleCore, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.core = core
        self.log = logging.getLogger()

        self.register_at_controller()
        # BEWARE there is already a channel named "validation", see validation search in skidata-hostcom
        self.core.messages.register_handler(b"validation_provider", ValidationRegisterRequestMessage,
                                            self.handle_validation_provider_register_request)

    def register_rpcs(self, rpc_server: RPCServer):
        rpc_server.add_filter(self._validation_provider_filter, "validation_provider", "validate")
        rpc_server.register_handler("validation_provider", "validate", request_class=ValidateRequest,
                                    response_class=ValidateResponse, handler=self.rpc_validate_ticket)

    def _validation_provider_filter(self, request, message, handler) -> bool:
        validation_provider = request.name
        if not validation_provider:
            return False
        return self.core.config.NAME == validation_provider

    def validate_ticket(self, request: ValidateRequest) -> ValidateResponse:
        """
        This method should validate a ticket for an occupant
        it should return a response with an error code if it fails
        :param request: ValidateRequest
        :return: ValidateResponse
        """
        raise NotImplementedError()

    def shutdown(self):
        self.unregister_at_controller()

    def rpc_validate_ticket(self, request: ValidateRequest, _) -> ValidateResponse:
        """
        Checks and validates a ticket for an occupant
        """

        response: ValidateResponse = self.validate_ticket(request)
        if response.cost_entries:
            cleaned_service_name: str = clean_service_name(self.core.config.NAME)
            for cost_entry in response.cost_entries:
                # if no source is set, source will be set to cleaned_service_name: e.g. "service_iocontroller"
                if cost_entry.get("source", None) is None:
                    cost_entry["source"] = cleaned_service_name

        return response

    def handle_validation_provider_register_request(self, _):
        """
        Registers the validation provider if the message type is register_request
        """
        self.register_at_controller()

    def register_at_controller(self):
        self.core.publish(ValidationRegisterMessage(), b"validation_provider")

    def unregister_at_controller(self):
        self.core.publish(ValidationUnregisterMessage(), b"validation_provider")
