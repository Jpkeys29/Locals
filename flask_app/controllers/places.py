from flask_app import app
from flask import render_template,redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.place import Place

@app.route('/place/create', methods=['POST'])
def create_place():
    if 'user_id' not in session:
        return redirect('/')
    place_diction = {
        'user_id': session['user_id'],
        'city': request.form['city'],
        'state': request.form['state'],
        'name':request.form['name'],
        'type': request.form['type'],
        'vibe': request.form['vibe'],
        'price': request.form['price'],
        'description': request.form['description'],
    }
    Place.Create_place(place_diction)
    return redirect ('/foreword')


@app.route('/myplaces')
def my_places():
    if 'user_id' not in session:
        return redirect('/')
    user_diction ={
        'id':session['user_id']
    }
    return render_template('myplaces.html', user= User.get_by_id(user_diction), all_places = Place.get_all_places())