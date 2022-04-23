from datetime import datetime
from email.policy import default
from pyparsing import nullDebugAction
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
import datetime


class BotUsers(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'bot_users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_tg_user = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    account_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    account = orm.relation('User')
    data_register = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)