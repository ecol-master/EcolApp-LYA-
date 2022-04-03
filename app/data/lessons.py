from gc import is_finalized
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    questions = sqlalchemy.Column(sqlalchemy.String, nullable=True) # "1 5 7 9"
    current_question = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) # "индекс данного вопроса в общем списке"
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    user = orm.relation("User")