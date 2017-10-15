"""Database"""
# pylint: disable=invalid-name
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError

from todo.config import DATABASE_URL, DEBUG


engine = create_engine(DATABASE_URL, echo=DEBUG)

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))


def create_tables():
    """Create tables"""
    from todo.models import Base
    test_connection()
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop tables"""
    from todo.models import Base
    test_connection()
    Base.metadata.drop_all(bind=engine)


def test_connection(max_attempts=5, interval_secs=1.0):
    """
    Test connection to database.

    If connection fails, retry after `interval_secs` for a total of `max_attempts`.
    """
    num_attempts = 1
    while True:
        try:
            with engine.connect():
                return

        except OperationalError:
            if num_attempts > max_attempts:
                msg = 'Connecting to database failed after {} attempts'.format(
                    max_attempts)
                print(msg)
                raise
            # Retry if connection refused
            num_attempts += 1
            time.sleep(interval_secs)
