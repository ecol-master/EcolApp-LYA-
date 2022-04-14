import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String) # имя пользователя
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True) # описание в профиле пользователя
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True) # почта под которой прошла регистрация
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True) # пароль
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True) # хэшированные пароль 
    data_registration = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True) # дата регистрации пользователя
    role_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("roles.id"), default=1)  # id роли пользователя

    # доп столбцы
    learned_lessons = sqlalchemy.Column(sqlalchemy.String, nullable=True) # список уроков которые прошел пользователь
    now_test_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("tests.id"))


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)