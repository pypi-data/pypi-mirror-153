from enum import Enum
from typing import List, Optional

from openmodule.models.base import OpenModuleModel, ZMQMessage, base64_validator, Gateway


class ValidateRequestTicketType(str, Enum):
    qr = "qr"
    nfc = "nfc"


class ValidateResponseState(str, Enum):
    ok = "ok"
    not_applicable = "not_applicable"


class ValidateResponseError(str, Enum):
    # the ticket is valid but it was already used once and cannot be used multiple times
    already_used = "already_used"

    # the ticket is invalid, e.g. the signature is incorrect
    invalid = "invalid"

    # the ticket is valid, but cannot be used for various reasons, please provide more
    # information in the `message` field in this case.
    excluded = "excluded"

    # is expired or cannot be used at this point in time
    expired = "expired"

    # an unknown error has occured while processing the ticket
    unknown_error = "unknown_error"


class ValidationRegisterRequestMessage(ZMQMessage):
    """
    sent by the controller as a request to all validation providers
    each validation provider who wants to register itself at the controller has to answer
    with a register message
    """
    type: str = "register_request"


class ValidationRegisterMessage(ZMQMessage):
    """
    sent by a validation provider if it wants to register itself at the controller
    """
    type: str = "register"


class ValidationUnregisterMessage(ZMQMessage):
    """
    sent by a validation provider if it shuts down and wants to unregister itself
    """
    type: str = "unregister"


class ValidateRequest(OpenModuleModel):
    name: str
    session_id: str
    type: ValidateRequestTicketType
    payload: str
    gateway: Optional[Gateway]

    _b64_payload = base64_validator("payload")


class ValidateCostEntry(OpenModuleModel):
    group: Optional[str] = None
    source: Optional[str] = None  # if None, source will be set to service name on default: e.g. "service_iocontroller"
    product_item_id: Optional[str] = None
    active: Optional[bool] = None
    delta_time_seconds: Optional[int] = None
    delta_amount: Optional[int] = None
    source_id: Optional[str] = None
    idempotency_key: Optional[str] = None


class ValidateResponse(OpenModuleModel):
    state: ValidateResponseState
    error: Optional[ValidateResponseError]
    cost_entries: Optional[List[dict]]
    message: Optional[str]
