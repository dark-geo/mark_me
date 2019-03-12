from database import db_api
from flask import Flask, redirect, url_for
from flask import request, make_response
from flask import render_template, send_from_directory

app = Flask(__name__)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def setcookie():
    username = request.form['username']

    resp = make_response(redirect('/index'))

    user_id = db_api.get_or_create_user(username)

    resp.set_cookie('user_id', str(user_id))

    return resp

@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/login'))

    resp.set_cookie('user_id', '')

    return resp


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    user_id = request.cookies.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/answer', methods=['POST'])
def answer():
    user_id = request.cookies.get('user_id')




if __name__ == '__main__':
    app.run(debug=True)