from datetime import datetime

from pydantic.main import BaseModel
from sqlalchemy import DateTime

from openmodule import config


class CheckingOpenModuleModel(type(BaseModel), type):
    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)

        # noinspection PyUnresolvedReferences
        for field_name, field in cls.__fields__.items():
            if field.type_ == datetime:
                assert "_timezone_validator" in field.class_validators, (
                    "datetime fields must use the timezone_validator to ensure all datetime values "
                    "are always naive. Otherwise runtime errors may occur depending on the isoformat used.\n"
                    f"In class {name}, please add:\n"
                    f'  _tz_{field_name} = timezone_validator("{field_name}")'
                )

        return cls


def check_invalid_database_column_type(typ):
    if config.run_checks():
        assert not isinstance(typ, DateTime), "Do NOT use DateTime fields, use TZDateTime fields instead"
