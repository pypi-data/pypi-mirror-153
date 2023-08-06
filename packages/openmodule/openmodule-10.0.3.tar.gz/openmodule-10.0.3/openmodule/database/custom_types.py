from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.sql.visitors import VisitableType
from sqlalchemy.types import TypeDecorator


class MetaOptions(VisitableType):
    """
    this behaves similarly to django's meta classes, but without any edge cases covered
    it is used for simple single inheritance without anything special in the alert type
    and package info classes
    """

    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)

        # EventModel
        if len(bases) == 1:
            if not getattr(bases[0], "_registry", None):
                setattr(bases[0], "_registry", dict())

            bases[0]._registry[x] = x.__module__
        return x


class CustomType(TypeDecorator, metaclass=MetaOptions):
    @classmethod
    def custom_import(cls, obj):
        for custom, mod in cls._registry.items():
            if type(obj) == custom:
                return mod, custom.__name__
        return None, None


class TZDateTime(CustomType):
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            assert not isinstance(value, datetime) or value.tzinfo is None, (
                "You need to convert a datetime to a naive time, because sqlite loses tz infos. "
            )
        return value
