"""Models"""
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from todo.database import session
from todo.constants import TO_DO

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


class Board(Base):
    """Board model"""
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    task_number = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False)
    tasks = relationship('Task', backref='board')

    def __init__(self, name):
        self.name = name
        self.task_number = 0


class Task(Base):
    """Task model"""
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False)
    board_id = Column(Integer, ForeignKey('boards.id'))

    def __init__(self, number, title, description, board_id, status=TO_DO):
        self.number = number
        self.title = title
        self.description = description
        self.status = status
        self.board_id = board_id
