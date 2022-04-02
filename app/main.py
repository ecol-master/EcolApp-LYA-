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
        return redirect('/success')
    return render_template('login_page.html', title='Авторизация', form=form)

if __name__ == "__main__":
    app.run()