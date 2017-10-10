"""Database"""
# pylint: disable=invalid-name

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


db_url = os.environ.get('DATABASE_URL')
if not db_url:
    raise Exception('`DATABASE_URL` environment variable not set.')

engine = create_engine(db_url, echo=True)

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))


def create_tables():
    """Create tables"""
    from todo.models import Base
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop tables"""
    from todo.models import Base
    Base.metadata.drop_all(bind=engine)
