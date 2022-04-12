import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True) # название урока
    title_image = sqlalchemy.Column(sqlalchemy.String, nullable=True) # картинка урока
    href = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # questions = sqlalchemy.Column(sqlalchemy.String, nullable=True) # "1 5 7 9"
    # current_question = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) # "индекс данного вопроса в общем списке"