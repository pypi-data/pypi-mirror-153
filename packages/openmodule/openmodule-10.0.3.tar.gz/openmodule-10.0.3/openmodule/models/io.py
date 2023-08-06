from datetime import datetime
from typing import Dict, Optional

from pydantic import Field

from openmodule.models.base import ZMQMessage, Gateway, OpenModuleModel, timezone_validator


class IoMessage(ZMQMessage):
    gateway: Gateway
    type: str
    pin: str
    value: int
    inverted: bool = False
    physical: Optional[int]
    edge: int
    pin_number: Optional[int]
    pin_label: Optional[str]
    meta: Dict = {}


class IoState(OpenModuleModel):
    gateway: Gateway
    type: str
    pin: str
    value: int
    inverted: bool
    physical: int
    last_timestamp: datetime
    _tz_last_timestamp = timezone_validator("last_timestamp")
