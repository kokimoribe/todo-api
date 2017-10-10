"""Models"""
# pylint: disable=invalid-name

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy import Column, Integer, String, DateTime, Enum, func

from todo.database import session
from todo.enums import Status


Base = declarative_base()
Base.query = session.query_property()


class Mixin:
    """Class that adds helper methods for serializing model instances"""

    @classmethod
    def columns(cls):
        """Return the names of the model's columns."""
        # Column names are returned in the same order as they
        # were defined in the model class definition.
        return inspect(cls).columns.keys()

    def to_dict(self):
        """Return dictionary representation of model instance."""
        return {column: getattr(self, column) for column in self.columns()}


class Task(Base, Mixin):
    """Task model"""
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(Status, name='task_status'), nullable=False)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now(),
                        nullable=False)

    def __init__(self, title, description, status=Status.TO_DO):
        self.title = title
        self.description = description
        self.status = status
