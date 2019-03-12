import random
from pathlib import Path
from uuid import UUID, uuid4
from database import session_context_manager
from database import entities



def get_username_by_id(user_id: UUID):
    with session_context_manager() as session:
        user = session.query(entities.User).filter_by(id=user_id).scalar()

        if not user:
            raise ValueError('There is no user with such ID in the database!')

    return user.username


def get_or_create_user(username: str) -> UUID:
    with session_context_manager() as session:
        user = session.query(entities.User).filter_by(username=username).scalar()

        if user:
            user_id = user.id
        else:
            user_id = uuid4()
            session.add(entities.User(username=username, id=user_id))

    return user_id



def get_random_cloud() -> UUID:
    with session_context_manager() as session:
        used_clouds_ids = [c_id for c_id, in session.query(entities.UsersClouds.cloud_id).distinct()]
        all_clouds_ids = [c_id for c_id, in session.query(entities.Cloud.id)]
        all_clouds_ids.extend(used_clouds_ids)

        cloud_id = random.choice(list(set(all_clouds_ids)))

    if not cloud_id:
        cloud_id = uuid4()

    return cloud_id


def set_cloud_answer(user_id: UUID, cloud_id: UUID, has_cloud: bool):
    with session_context_manager() as session:
        user = session.query(entities.User).filter_by(id=user_id).scalar()
        cloud = session.query(entities.Cloud).filter_by(id=cloud_id).scalar()

        if not user or not cloud:
            raise ValueError('There is no user or cloud with such ID in the database!')

        session.add(entities.UsersClouds(user_id=user_id,
                                         cloud_id=cloud_id,
                                         has_cloud=has_cloud))


def get_path_to_picture(cloud_id: UUID) -> str:
    with session_context_manager() as session:
        cloud = session.query(entities.Cloud).filter_by(id=cloud_id).scalar()

        if not cloud:
            raise ValueError('There is no cloud with such ID in the database!')

    return cloud.path_to_file



def load_clouds_to_db(root_dir: Path):
    with session_context_manager() as session:
        for p in root_dir.glob('**/*.png'):
            session.add(entities.Cloud(path_to_file=str(p)))
