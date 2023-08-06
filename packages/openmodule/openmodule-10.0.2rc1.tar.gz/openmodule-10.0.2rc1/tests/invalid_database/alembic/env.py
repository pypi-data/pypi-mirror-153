from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

from openmodule.database.database import run_env_py

Base = declarative_base()


class DatabaseInvalidTimezoneTestModel(Base):
    __tablename__ = "test_timezone_invalid"
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=True)


run_env_py([Base])
