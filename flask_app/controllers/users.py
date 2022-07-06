from crypt import methods
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

@app.route('/login', methods=['POST'])
def login():
    user_from_db = user.User.get_by_email({'email': request.form['email']})
    if user_from_db and bcrypt.check_password_hash(user_from_db.password, request.form ['password']):
        session['user_id'] = user_from_db.id
        return redirect('/foreword')
    else:
        flash("Invalid email/password", 'login')
        return redirect('/')

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
    user_diction ={
        'id':session['user_id']
    }
    return render_template('local.html', user= User.get_by_id(user_diction))

@app.route('/visit')
def visit():
    if 'user_id' not in session:
        return redirect('/')
    user_diction ={
        'id':session['user_id']
    }
    return render_template('visiting.html', user= User.get_by_id(user_diction))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

