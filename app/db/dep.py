from typing import Iterator
from sqlalchemy.orm import Session
from app.db.connection import MySqlSession
from app.cache.time_cache import time_cache


def get_db() -> Iterator[Session]:
    """
        Dependency that gets a cached database session.
    """
    session = _get_session()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()


@time_cache(max_age_seconds=60 * 10)
def _get_session():
    return MySqlSession()
