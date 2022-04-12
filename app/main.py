import json
import random

from flask import Flask, redirect, render_template
from flask_login import LoginManager, current_user, login_user
from flask_wtf import FlaskForm
from numpy import add, less

from data import db_session
from data.lessons import Lesson
from data.users import User
from forms.user import LoginForm, RegisterForm
from data.tests import Test
from data.questions import Question

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
        return render_template('login_page.html',
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
            nickname=form.name.data,
            email=form.email.data,
            description=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/study')
    return render_template('register_page.html', title='Регистрация', form=form)


def add_lessons():
    lessons = [
        {"title":"Экология", 
        "title_image":"../static/images/logo_welcome_page.svg",
        "href":"../study/ecology" 
        },
        {"title":"Земля", 
        "title_image":"../static/images/logo_welcome_page.svg",
        "href":"../study/eath" 
        },
        {"title":"Вода", 
        "title_image":"../static/images/logo_welcome_page.svg", 
        "href":"../study/water"
        },
        {"title":"Небо", 
        "title_image":"../static/images/logo_welcome_page.svg", 
        "href":"../study/sky"
        }
    ]

    
    for lesson in lessons:
        lesson_db = Lesson()
        lesson_db.title = lesson["title"]
        lesson_db.title_image = lesson["title_image"]
        lesson_db.href = lesson["href"]
        db_sess.add(lesson_db)
        db_sess.commit()

def add_questions():
    file_question = open("templates/questions.json")
    all_questions = json.load(file_question)
    for quiz in all_questions["questions"]:
        quiz_db = Question()
        quiz_db.text = quiz["text"]
        quiz_db.rigth_answer = quiz["answer"]
        quiz_db.points = 5
        db_sess.add(quiz_db)
        db_sess.commit()


# обработчик при переходе на страницу уроков
@app.route('/study')
def learn():
#     user_id = current_user.id
    add_lessons()
    lessons = db_sess.query(Lesson).all()
    return render_template("study_page.html", lessons=lessons)

@app.route("/study/<lesson>")
def show_lesson(lesson):
    add_questions()
    questions_for_test = random.choices([str(q.id) for q in db_sess.query(Question).all()], k=5)

    new_test = Test()
    new_test.questions = ' '.join(questions_for_test)
    new_test.current_question = 0

    try:
        new_test.user_id = current_user.id

        
        db_sess.add(new_test)
        db_sess.commit()

        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.now_test_id = new_test.id
        db_sess.commit(user)
    except Exception:   
        db_sess.add(new_test)
        db_sess.commit()

    question = db_sess.query(Question).filter(Question.id == int(questions_for_test[0])).first()
    return render_template("lesson_page.html", question=question)

@app.route("/study/<lesson>/<int:num_question>")
def show_new_question():
    pass


if __name__ == "__main__":
    app.run()
