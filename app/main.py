from flask import Flask

app = Flask(__name__)

@app.route("/learn/<user_id:int>")
def load_learn():
    pass

if __name__ == "__main__":
    app.run()