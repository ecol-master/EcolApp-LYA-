from enum import unique
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Roles(SqlAlchemyBase):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True) # id пользователя, будет указываться в бд
    title = sqlalchemy.Column(sqlalchemy.String, unique=True) # текст роли     
