from flask import Flask
from flask import render_template, send_from_directory

app = Flask(__name__)


@app.route('/login', methods=['GET'])
def start_page():
    return render_template('login.html')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()