from flask import Flask, redirect, url_for
from flask import request, make_response
from flask import render_template, send_from_directory

app = Flask(__name__)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def setcookie():
    
    user = request.form['name']

    resp = make_response(render_template('index.html'))

    resp.set_cookie('user_id', user)

    return resp

@app.route('/logout', methods=['GET'])
def logout():

    resp = make_response(render_template('login.html'))

    resp.set_cookie('user_id', '')

    return resp


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    user_id = request.cookies.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run()