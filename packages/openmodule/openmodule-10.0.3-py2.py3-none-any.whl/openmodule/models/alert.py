from enum import Enum

from pydantic import validator
from typing import Dict, Optional

from openmodule.models.base import ZMQMessage


class AlertStatus(str, Enum):
    ok = "ok"
    error = "error"
    offline = "offline"


class AlertHandleType(str, Enum):
    state = "state"
    state_change = "state_change"
    count = "count"


class AlertMessage(ZMQMessage):
    type: str = "alert"
    status: AlertStatus
    alert_meta: Dict
    package: str
    alert_type: str
    source: Optional[str]
    handle_type: AlertHandleType
    value: Optional[float]

    @validator("value")
    def require_value_for_state_type(cls, v, values):
        if values["handle_type"] == AlertHandleType.state:
            assert v is not None, "value must not be None for alerts with handle_type='state'"
        return v
