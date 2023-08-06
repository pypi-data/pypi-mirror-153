import uuid

from sqlalchemy import Column, String, Integer, Date, Time
from sqlalchemy.ext.declarative import declarative_base

from openmodule.database.custom_types import TZDateTime

Base = declarative_base()


class DatabaseTestModel(Base):
    __tablename__ = "test"
    id = Column(String, default=lambda: str(uuid.uuid4()), unique=True, primary_key=True)
    value1 = Column(Integer, default=1)
    value2 = Column(Integer, default=2)
    string = Column(String, default="initial")


class DatabaseTimezoneTestModel(Base):
    __tablename__ = "test_timezone"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tz_datetime = Column(TZDateTime, nullable=True)
    date = Column(Date, nullable=True)
    time = Column(Time, nullable=True)
