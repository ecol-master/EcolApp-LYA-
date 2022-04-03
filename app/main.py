from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from forms.user import LoginForm, RegisterForm
from data import db_session
from data.users import User
from flask_login import login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init("db/users.db")
db_sess = db_session.create_session()

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
            return redirect("/learn")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_page.html', form=form)


# начал делать форму для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect('/learn')
    return render_template('register_page.html', title='Авторизация', form=form)

@app.route('/learn')
def learn():
    pass

# some changes

if __name__ == "__main__":
    app.run()