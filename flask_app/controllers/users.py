from flask import render_template, redirect, request, session,flash
from flask_app import app
from flask_app.models import user
from flask_app.models.user import User
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_route():
    return render_template('login.html')

@app.route('/user/create', methods=['POST'])
def create_user():
    print("BUGGING",request.form['first_name'])
    print("BUGGING",request.form['last_name'])
    print("BUGGING",request.form['email'])
    if not User.validate_user(request.form):
        return redirect('/')
    user_data ={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email':request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
    }
    session['user_id'] = User.create(user_data)
    return redirect('/foreword')

@app.route('/foreword')
def foreword():
    if 'user_id' not in session:
        return redirect('/')
    user_diction ={
        'id':session['user_id']
    }
    return render_template('foreword.html', user= User.get_by_id(user_diction))

@app.route('/local')
def local():
    if 'user_id' not in session:
        return redirect('/')
    render_template('local.html')
