from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from forms.user import LoginForm, RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/')
def start_site():
    return render_template('welcome_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/learn/<user_id:int>')
    return render_template('login_page.html', title='Авторизация', form=form)


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


if __name__ == "__main__":
    app.run()