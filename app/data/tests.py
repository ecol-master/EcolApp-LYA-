import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import datetime


class Test(SqlAlchemyBase):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    questions = sqlalchemy.Column(sqlalchemy.String, nullable=True) # "1 5 7 9"
    current_question = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) # "индекс данного вопроса в общем списке"
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date_of_completion = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)