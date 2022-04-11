from django.shortcuts import render
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from forms.user import LoginForm, RegisterForm
from data import db_session
from data.users import User
from flask_login import login_user, LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/users.db")
db_sess = db_session.create_session()

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def start_site():
    return render_template('welcome_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/study")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_page.html', form=form)


# начал делать форму для регистрации
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        print("зашел сюда")
        if form.password.data != form.password_again.data:
            print("Пароли не совпадают")
            return render_template('register_page.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
            
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            print("Такой пользователь уже есть")
            return render_template('register_page.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            description=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/study')
    return render_template('register_page.html', title='Регистрация', form=form)

@app.route('/study')
def learn():
    return render_template("study_page.html")

# some changes

if __name__ == "__main__":
    app.run()