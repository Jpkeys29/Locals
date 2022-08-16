from crypt import methods
from flask_app import app
from flask import render_template,redirect, session, request,flash
from flask_app.models.user import User
from flask_app.models.place import Place

@app.route('/place/create', methods=['POST'])
def create_place():
    if 'user_id' not in session:
        return redirect('/')
    if not Place.validate_place(request.form):
        return redirect('/local')
    place_diction = {
        'user_id': session['user_id'], #ID of person who's logged in
        'city': request.form['city'],
        'state': request.form['state'],
        'name':request.form['name'],
        'type': request.form['type'],
        'vibe': request.form['vibe'],
        'price': request.form['price'],
        'description': request.form['description'],
    }
    Place.create_place(place_diction)
    return redirect ('/home')

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    user_diction ={
        'id':session['user_id']
    }
    return render_template('home.html', user= User.get_by_id(user_diction),places = Place.get_all_places())


# @app.route('/myplaces')
# def my_places():
#     if 'user_id' not in session:
#         return redirect('/')
#     user_diction ={
#         'id':session['user_id']
#     }
#     return render_template('myplaces.html', user= User.get_by_id(user_diction),place = Place.get_all_places_with_reviewers())

@app.route('/myplaces/')
def my_places():
    if 'user_id' not in session:
        return redirect('/')
    user_diction ={
        'id':session['user_id']
    }
    return render_template('myplaces.html', user= User.get_by_id(user_diction),place = Place.get_all_places_with_reviewers())



@app.route("/places/goplaces", methods=['POST'])
def goplaces():
    if 'user_id' not in session:
        return redirect('/')
    user_diction ={
        'id':session['user_id']
    }
    place_diction ={
        'user_id': session['user_id'],
        'city': request.form['city'],
        'state':session['state'],
        'name':session['name'],
        'type':session['type'],
        'vibe':session['vibe'],
        'price':session['price'],
        'description':session['description'],
    }
    Place.get_all_from_one_city(place_diction)
    return redirect('/placereview')

@app.route('/placereview')
def place_review():
    if 'user_id' not in session:
        return redirect('/')
    place_diction ={
        'id':id
    }
    return render_template('placereview.html',user= User.get_by_id(place_diction),places = Place.get_all_from_one_city())

@app.route("/viewplaces/<int:id>")
def view_place_page(id):
    if 'user_id' not in session:
        return redirect('/')
    place_diction = {
        'id':id  #this is the id of the place
    }
    return render_template('viewplaces.html', place = Place.get_place_one_user(place_diction))
    
