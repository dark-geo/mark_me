from uuid import UUID
from pathlib import Path
from database import session_context_manager
from database import entities


def get_or_create_user(username: str) -> UUID:
    with session_context_manager() as session:
        user = session.query(entities.User).filter_by(name=username).scalar()
        if not user:
            pass


def init_clouds(path_to_pics: Path):
    with session_context_manager() as session:
        pass


