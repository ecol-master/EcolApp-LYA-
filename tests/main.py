from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def start_site():
    learn_url='https://stepik.org/'
    test_link='https://translate.google.com/?hl=ru&sl=en&tl=ru&op=translate'
    test_2link='http://127.0.0.1:5000/learn'
    return render_template('index.html', learn_url=learn_url, 
    test_link=test_link, test_2link=test_2link)

@app.route('/learn')
def learn():
    return render_template

if __name__ == "__main__":
    app.run()