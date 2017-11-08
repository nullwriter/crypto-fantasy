from contextlib import contextmanager
from sqlalchemy.orm import Session
from controller import BOT_ORM_SESSION

@contextmanager
def session_scope(obj=""):
    """Provide a transactional scope around a series of operations."""

    if obj:
        session = Session.object_session(obj)
    else:
        session = BOT_ORM_SESSION()
        session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
