import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database.entities import BaseModel


DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:1234@localhost:55432/mark_me')

engine: Engine = create_engine(DATABASE_URI)
session_factory: sessionmaker = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def session_context_manager():
    """Provide a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
