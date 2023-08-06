from enum import Enum
from typing import Optional, List

from openmodule.models.base import ZMQMessage, OpenModuleModel


class AnonymizeMessage(ZMQMessage):
    type: str = "anonymize"
    session_id: Optional[str]
    vehicle_ids: Optional[List[str]] = []


class AnonymizeRequest(OpenModuleModel):
    session_ids: List[str]


class AnonymizeResponse(OpenModuleModel):
    pass


class AnonymizeType(str, Enum):
    lpr = ":anonymize:lpr"
    phone = ":anonymize:phone"
    address = ":anonymize:address"
    name = ":anonymize:name"
    default = ":anonymize:"

    @staticmethod
    def get_for_type(typ):
        try:
            return AnonymizeType(typ)
        except ValueError:
            return AnonymizeType.default

    @staticmethod
    def get_string_for_type(typ):
        return str(AnonymizeType.get_for_type(typ))

    @staticmethod
    def get_type(string):
        return string.replace(AnonymizeType.default.value, "") or None

    def __str__(self):
        return self.value
