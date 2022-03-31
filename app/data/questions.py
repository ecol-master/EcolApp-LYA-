import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

class Question(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rigth_answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    points = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
