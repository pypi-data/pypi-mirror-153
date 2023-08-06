from typing import List

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DatabaseCascadeDeleteParentModel(Base):
    __tablename__ = "cascade_delete_parent"
    id = Column(Integer, primary_key=True, autoincrement=True)
    children: List['DatabaseCascadeDeleteChildModel'] = relationship("DatabaseCascadeDeleteChildModel",
                                                                     back_populates="parent",
                                                                     cascade="all, delete", passive_deletes=True)
    name = Column(Integer, nullable=True)


class DatabaseCascadeDeleteChildModel(Base):
    __tablename__ = "cascade_delete_child"
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey("cascade_delete_parent.id", ondelete="CASCADE"))
    parent = relationship("DatabaseCascadeDeleteParentModel", back_populates="children")
