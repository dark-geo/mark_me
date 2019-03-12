from uuid import UUID, uuid4
from pathlib import Path
from database import session_context_manager
from database import entities


def get_or_create_user(username: str) -> UUID:
    with session_context_manager() as session:
        user = session.query(entities.User).filter_by(username=username).scalar()

        if user:
            user_id = user.id
        else:
            user_id = uuid4()
            session.add(entities.User(username=username, id=user_id))

    return user_id


def init_clouds(path_to_pics: Path):
    with session_context_manager() as session:
        pass


def get_cloud_image():
    with session_context_manager() as session:
        pass


def set_answer(user_id: UUID, cloud_id: UUID):
    with session_context_manager() as session:
        pass

