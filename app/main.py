import json

from flask import Flask, redirect, render_template
from flask_login import LoginManager, current_user, login_user
from data import db_session
from data.lessons import Lesson
from data.users import User
from forms.user import LoginForm, RegisterForm, QuestionForm
from data.tests import Test
from data.questions import Question
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/users.db")
db_sess = db_session.create_session()

 

def write_file(text):
    with open("write.txt", mode="w") as file:
        file.write(text)

def check_is_auth():
    try:
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        return True
    except Exception:
        return False

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
        if form.password.data != form.password_again.data:
            return render_template('register_page.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
            
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
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
        return redirect('/login')
    return render_template('register_page.html', title='Регистрация', form=form)


def add_lessons():
    lessons = [
        {"title":"Экология", 
        "title_image":"../static/images/logo_welcome_page.svg",
        "href":"../study/ecology",
        "description":"Урок для изучения экологии",
        "href_name":"ecology" 
        },
        {"title":"Земля", 
        "title_image":"../static/images/logo_welcome_page.svg",
        "href":"../study/eath",
        "description":"Урок для изучения экологии",
        "href_name":"eath"  
        },
        {"title":"Вода", 
        "title_image":"../static/images/logo_welcome_page.svg", 
        "href":"../study/water",
        "description":"Урок для изучения экологии",
        "href_name":"water" 
        },
        {"title":"Небо", 
        "title_image":"../static/images/logo_welcome_page.svg", 
        "href":"../study/sky", 
        "description":"Урок для изучения экологии",
        "href_name":"sky" 
        }
    ]

    
    for lesson in lessons:
        lesson_db = Lesson()
        lesson_db.title = lesson["title"]
        lesson_db.title_image = lesson["title_image"]
        lesson_db.href = lesson["href"]
        lesson_db.description = lesson["description"]
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
    # add_lessons()
    if not check_is_auth():
        return redirect("/")
    lessons = db_sess.query(Lesson).all()
    return render_template("study_page.html", lessons=lessons)

@app.route("/study/<lesson>")
def show_lesson(lesson):
    add_questions()
    if not check_is_auth():
        return redirect("/")
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
    return redirect(f"/study/{lesson}/1")

@app.route("/study/<lesson>/<int:num_question>",  methods=['GET', 'POST'])
def show_new_question(lesson, num_question):
    if not check_is_auth():
        return redirect("/")
    write_file("здесь")

    user = db_sess.query(User).filter(User.id == current_user.id).first()
    test_id = user.now_test_id
    test = db_sess.query(Test).filter(Test.id == test_id).first()   
    
    question_id = int(test.questions.split()[test.current_question])
    question = db_sess.query(Question).filter(Question.id == question_id).first()
    
    question_form = QuestionForm()
    if question_form.validate_on_submit():
        write_file("зашел во внутрь")
        if num_question  ==  len(test.questions.split()):
            write_file("проверил")
            return redirect("/end_test")
        else:
            if question.rigth_answer != question_form.user_answer.data:
               test.is_loyal = False
               db_sess.commit() 
            test.current_question += 1
            db_sess.commit()
            write_file("дошел до переадресации")
            return redirect(f"/study/{lesson}/{test.current_question + 1}")
    return render_template("lesson_page.html", form=question_form, question=question, num_question=num_question, len_questions=len(test.questions.split()))


@app.route("/end_test")
def end_test():

    test = db_sess.query(Test).filter(Test.id == current_user.now_test_id).first()
    return render_template("end_test_page.html", test=test)

if __name__ == "__main__":
    app.run()
