import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    data_registration = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    