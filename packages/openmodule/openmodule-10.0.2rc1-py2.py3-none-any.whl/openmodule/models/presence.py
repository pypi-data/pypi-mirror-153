from datetime import datetime
from typing import Optional, List, Union

from pydantic import Field

from openmodule.models.base import ZMQMessage, OpenModuleModel, Gateway, timezone_validator
from openmodule.models.vehicle import Medium, LPRMedium, MakeModel, PresenceAllIds, EnterDirection


class PresenceMedia(OpenModuleModel):
    lpr: Optional[LPRMedium]
    qr: Optional[Medium]
    nfc: Optional[Medium]
    pin: Optional[Medium]


class PresenceBaseData(OpenModuleModel):
    vehicle_id: int
    source: str
    present_area_name: str = Field(..., alias="present-area-name")
    last_update: datetime
    gateway: Gateway
    medium: PresenceMedia
    make_model: Optional[MakeModel]
    all_ids: PresenceAllIds
    enter_direction: EnterDirection = EnterDirection.unknown

    _tz_last_update = timezone_validator("last_update")

    class Config:
        # allows setting attributes both via the alias, and the field name.
        # is used to rename old variables which are hard to understand by their name (e.g. id -> medium id)
        allow_population_by_field_name = True


class PresenceBaseMessage(PresenceBaseData, ZMQMessage):
    pass


class PresenceBackwardMessage(PresenceBaseMessage):
    type: str = "backward"
    unsure: bool = False
    leave_time: datetime = Field(..., alias="leave-time")
    bidirectional_inverse: bool = False

    _tz_leave_time = timezone_validator("leave_time")


class PresenceForwardMessage(PresenceBaseMessage):
    type: str = "forward"
    unsure: bool = False
    leave_time: datetime = Field(..., alias="leave-time")
    bidirectional_inverse: bool = False

    _tz_leave_time = timezone_validator("leave_time")


class PresenceLeaveMessage(PresenceBaseMessage):
    type: str = "leave"
    num_presents: int = Field(0, alias="num-presents")


class PresenceEnterMessage(PresenceBaseMessage):
    type: str = "enter"


class PresenceChangeMessage(PresenceBaseMessage):
    type: str = "change"
    change_vehicle_id: Optional[bool]


class PresenceRPCRequest(OpenModuleModel):
    gate: str


class PresenceRPCResponse(OpenModuleModel):
    presents: List[PresenceBaseData]
