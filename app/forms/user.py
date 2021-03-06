from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class QuestionForm(FlaskForm):
    user_answer = StringField("Ответ")
    button_next = SubmitField("Следующий вопрос")

class CreateArticleForm(FlaskForm):
    title_article = StringField("Title")
    text_article = TextAreaField("Your Story")
    submit = SubmitField('Publish')

class CreateNewsForm(FlaskForm):
    title_news = StringField("Title")
    text_news = TextAreaField("Your Story")
    submit = SubmitField('Publish')
