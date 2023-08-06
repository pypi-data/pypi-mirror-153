import re
from datetime import datetime, timedelta, tzinfo
from enum import Enum
from typing import List, Optional, Union, Dict

from dateutil import rrule, tz
from dateutil.parser import parse
from dateutil.rrule import rrulestr
from dateutil.tz import UTC
from pydantic import validator, Field

from openmodule.models.base import OpenModuleModel, ZMQMessage, Gateway, timezone_validator, datetime_to_timestamp


class MediumType(str, Enum):
    lpr = "lpr"
    nfc = "nfc"
    pin = "pin"
    qr = "qr"


class AccessCategory(str, Enum):
    booked_digimon = "booked-digimon"
    booked_employee = "booked-employee"
    booked_visitor = "booked-visitor"
    permanent_digimon = "permanent-digimon"
    permanent_employee = "permanent-employee"
    filler_employee = "filler-employee"
    filler_digimon = "filler-digimon"
    filler_visitor_button = "filler-visitor-button"
    filler_visitor_unexpected = "filler-visitor-unexpected"
    unknown_category = "unknown-category"


def check_recurrence(cls, recurrence, values, **kwargs):
    if recurrence:
        if not values.get("duration"):
            raise ValueError("set a duration when using recurrence")

        try:
            if "DTSTART" not in recurrence:
                raise ValueError("recurrence must contain a DTSTART field")
            if "\n" not in recurrence:
                raise ValueError("DTSTART must be separated by a newline '\\n' character")

            rrule.rrulestr(recurrence)
        except Exception as e:
            raise ValueError(f"recurrence is not valid '{e}'") from None
        return recurrence
    else:
        return None


class Access(OpenModuleModel):
    category: AccessCategory
    start: datetime
    end: Optional[datetime] = None
    duration: Optional[int] = Field(description="duration in seconds, starting with the start time of the "
                                                "recurrence. Required if recurrence is set.")
    recurrence: Optional[str]
    zone: Optional[str]
    occupant_check: bool = False
    infos: Optional[dict] = {}
    cost_entries: List[dict] = []
    clearing: Optional[str]
    user: str

    _check_recurrence = validator("recurrence", allow_reuse=True)(check_recurrence)
    _tz_start = timezone_validator("start")
    _tz_end = timezone_validator("end")

    _rrule_regex = re.compile(r"\s*DTSTART[:|=]+([\d\w+:]*)\s*[\n|;]*", re.IGNORECASE)

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data["start"] = datetime_to_timestamp(data["start"])
        if data.get("end") is not None:
            data["end"] = datetime_to_timestamp(data["end"])
        return data

    def _recurrence_is_valid_at(self, native_utc_dt: datetime, timezone):
        if isinstance(timezone, str):
            timezone = tz.gettz(timezone)

        # we first construct a rrule object with dtstart as a naive localized datetime
        dtstart_string = self._rrule_regex.search(self.recurrence).group(1)
        dtstart_utc = parse(dtstart_string).replace(tzinfo=UTC)
        local_dtstart = dtstart_utc.astimezone(timezone)
        naive_dtstart = local_dtstart.replace(tzinfo=None)
        recurrence_without_dtstart = self._rrule_regex.sub("", self.recurrence)
        recurrence = rrulestr(recurrence_without_dtstart, dtstart=naive_dtstart, cache=True)

        # get the nearest event before our desired timestamp
        local_dt = native_utc_dt.replace(tzinfo=UTC).astimezone(timezone)
        naive_dt = local_dt.replace(tzinfo=None)
        naive_before = recurrence.before(naive_dt, inc=True)
        if not naive_before:
            return False

        # calculate the start/end of the recurrent event
        local_before = naive_before.replace(tzinfo=timezone)
        local_after = local_before + timedelta(seconds=self.duration)

        # in case the utc offset jumps (dst change) we always add the time difference here, because there are two
        # groups of users, and we want to work for both
        # given a dst change at 03:00 back to 02:00:
        # a) user A always arrives at 02:00, and stays 2 hours, he does not care if a dst change happened, he always
        #    stays 2 hours, regardless of the dst change, for him `start + timedelta(hours=2)` would work
        # b) user B always arrives at 04:00, so he does not care that there has been an extra hour between 2 and 4
        # oclock, he arrives at 04:00. For hom `start + timedelta(hours=2)` would miss by an hour
        utc_offset_diff = abs(local_before.utcoffset() - local_after.utcoffset())
        if utc_offset_diff.total_seconds() != 0:
            local_after += utc_offset_diff
        naive_after = local_after.replace(tzinfo=None)

        return naive_before <= naive_dt < naive_after

    def is_valid_at(self, dt: datetime, timezone: Union[str, tzinfo]):
        if dt.tzinfo:
            dt = dt.astimezone(UTC).replace(tzinfo=None)

        if self.end:
            between_start_and_end = self.start <= dt <= self.end
        else:
            between_start_and_end = self.start <= dt

        if self.recurrence:
            return between_start_and_end and self._recurrence_is_valid_at(dt, timezone)
        else:
            return between_start_and_end


class BackendRegisterRequestMessage(ZMQMessage):
    """
    sent by the controller as a request to all backends
    each backend who wants to register itself at the controller has to answer
    with a register message
    """
    type: str = "register_request"


class BackendRegisterMessage(ZMQMessage):
    """
    sent by a backend if it wants to register itself at the controller
    """
    type: str = "register"


class BackendUnregisterMessage(ZMQMessage):
    """
    sent by a backend if it shuts down and wants to unregister itself
    """
    type: str = "unregister"


class AccessRequest(OpenModuleModel):
    """
    The AccessRequest Model
    """
    name: str
    gateway: Optional[Gateway] = None
    medium_type: MediumType
    medium_id: str = Field(..., alias="id")

    class Config:
        # allows setting attributes both via the alias, and the field name.
        # is used to rename old variables which are hard to understand by their name (e.g. id -> medium id)
        allow_population_by_field_name = True


class MediumAccesses(OpenModuleModel):
    accesses: List[Access]
    medium_id: str = Field(..., alias="id")
    medium_type: str = Field(..., alias="type")

    class Config:
        # allows setting attributes both via the alias, and the field name.
        # is used to rename old variables which are hard to understand by their name (e.g. id -> medium id)
        allow_population_by_field_name = True


class AccessResponse(OpenModuleModel):
    success: bool = False
    medium: MediumAccesses


class CountMessage(ZMQMessage):
    type: str = "count"
    user: str
    gateway: Gateway
    medium_type: MediumType
    medium_id: str = Field(..., alias="id")
    count: int
    transaction_id: str
    zone: str
    category: AccessCategory
    real: bool
    vehicle_id: Optional[str]
    infos: Optional[dict]
    access_data: Optional[dict]
    error: Optional[str]
    previous_transaction_id: Optional[List[str]]  # double_entry, choose_random error
    previous_user: Optional[str]  # user_changed error
    previous_medium_type: Optional[str]  # medium_changed, medium_id_changed error
    previous_medium_id: Optional[str] = Field(None,  # medium_changed, medium_id_changed error
                                              alias="previous_medium_id")
    chosen: Optional[dict]  # choose_random error

    class Config:
        # allows setting attributes both via the alias, and the field name.
        # is used to rename old variables which are hard to understand by their name (e.g. id -> medium id)
        allow_population_by_field_name = True


class SessionStartMessage(ZMQMessage):
    type: str = "start"

    id: str
    user_id: Optional[str]
    zone_id: str
    cost_table: dict
    clearing: Optional[str]
    access_infos: Optional[dict]
    serviceable: bool

    entry_time: datetime
    entry_data: Dict

    _tz_entry_time = timezone_validator("entry_time")


class SessionFinishMessage(ZMQMessage):
    type: str = "finish"

    id: str
    user_id: Optional[str]
    zone_id: str
    cost_table: dict
    clearing: Optional[str]
    access_infos: Optional[dict]
    serviceable: bool

    entry_time: datetime
    entry_data: Dict
    exit_time: datetime
    exit_data: Dict

    payment_lock_at: Optional[datetime]
    payment_lock_until: Optional[datetime]

    _tz_entry_time = timezone_validator("entry_time")
    _tz_exit_time = timezone_validator("exit_time")
    _tz_payment_lock_at = timezone_validator("payment_lock_at")
    _tz_payment_lock_until = timezone_validator("payment_lock_until")
