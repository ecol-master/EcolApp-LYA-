import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class BotUsers(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'bot_users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_tg_user = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)