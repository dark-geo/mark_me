from pathlib import Path
from uuid import UUID
from database import db_api
from flask import Flask, redirect, url_for, send_file
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

    username = db_api.get_username_by_id(UUID(user_id))
    cloud_id = db_api.get_random_cloud()


    return render_template('index.html',
                           username=username,
                           user_id=str(user_id),
                           cloud_id=str(cloud_id))


@app.route('/clouds/<uuid:cloud_id>', methods=['GET'])
def get_cloud_pic(cloud_id):
    path_to_pic = db_api.get_path_to_picture(cloud_id)

    return send_file(str(path_to_pic), mimetype='image/png')


@app.route('/answer/<uuid:user_id>/<uuid:cloud_id>', methods=['POST'])
def answer(user_id, cloud_id):
    has_cloud = True if request.form['answer'] == 'true' else False

    db_api.set_cloud_answer(user_id, cloud_id, has_cloud)

    resp = make_response(redirect('/index'))

    return resp



if __name__ == '__main__':
    app.run(debug=True)