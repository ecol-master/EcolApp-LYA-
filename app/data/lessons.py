import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True) # название урока
    title_image = sqlalchemy.Column(sqlalchemy.String, nullable=True) # картинка урока
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True) # описание урока
    href = sqlalchemy.Column(sqlalchemy.String, nullable=True) # ссылка на урок
    href_name = sqlalchemy.Column(sqlalchemy.String, nullable=True) # имя в пути (нужно для определения в декораторе)