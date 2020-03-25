from flask import Flask, url_for, session, render_template, request, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'login'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/login'

mongo = PyMongo(app)

@app.route('/index', methods=['GET'])
def index():
    if 'username' in session:
        return f'You are logged in as {session["username"]}'

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        db_pwd = login_user['password']
        curr_pwd = bcrypt.hashpw(request.form['pass'].encode('utf-8'), db_pwd)
        if curr_pwd == db_pwd:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'invalid username/password'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name':request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return  'username already exist!'

    return render_template('register.html')


if __name__=='__main__':
    app.secret_key = 'my_secret'
    app.run(debug=True)

