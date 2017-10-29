"""Models"""
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Integer, String, DateTime, func, MetaData
from sqlalchemy.ext.declarative import declarative_base

from todo.database import session
from todo.enums import Status


# Define convention for naming constraints
# This convention will be used by Alembic when new constraints are added
# Reference:
# http://docs.sqlalchemy.org/en/latest/core/constraints.html#configuring-constraint-naming-conventions
# http://alembic.zzzcomputing.com/en/latest/naming.html#the-importance-of-naming-constraints
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base = declarative_base()
Base.metadata = MetaData(naming_convention=convention)
Base.query = session.query_property()


class Task(Base):
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
