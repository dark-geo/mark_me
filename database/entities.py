"""
Модуль :py:mod:`database.entities` содержит в себе классы сущностей объектной модели БД.
А также вспомогательные функции для сериализации объектной модели.
"""

from typing import Set, Dict

from sqlalchemy import Column, DateTime, String, Enum, inspect, text, UniqueConstraint, Table
from sqlalchemy import Integer, Float, Boolean, ForeignKey, func, JSON, Date, FLOAT, ARRAY
from sqlalchemy.dialects.postgresql import UUID, INTERVAL
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy_mixins import AllFeaturesMixin


Base = declarative_base()


# сущности, связанные напрямую с wellfield #########################################
class BaseModel(Base, AllFeaturesMixin):
    # language=rst
    """
    Базовая модель.

    Класс, описывающий базовую модель.

    :var datetime.datetime _created: дата создания объекта;
    :var datetime.datetime _updated: дата обновления объекта;
    :var uuid.UUID id: уникальный id объекта;
    """
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))

    @property
    def column_attributes(self) -> Set:
        # language=rst
        """
        Получение множества аттрибутов, соответствующих аттрибутам соответствующей таблицы из базы.

        :return set:
        """

        return set(inspect(self).mapper.column_attrs.keys())


class User(BaseModel):
    # language=rst
    """
    Пользователи.

    :var str username: логин;
    """
    __tablename__ = 'users'

    username = Column('username', String(255), unique=True)


class Cloud(BaseModel):
    __tablename__ = "clouds"

    path_to_file = Column('path_to_file', String(1024), nullable=False)


class UsersClouds(BaseModel):
    __tablename__ = 'users_clouds'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    cloud_id = Column(UUID(as_uuid=True), ForeignKey('clouds.id', ondelete='CASCADE'))
    has_cloud = Column('has_cloud', Boolean, default=False)
