from flask_app import app
from flask import render_template,redirect, session, request,flash
from flask_app.models.user import User
from flask_app.models.place import Place
# import requests
# from gitignore import API KEY


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

#DUPLICATE (FEEL FREE TO EDIT)
@app.route('/myplaces/')
def my_places():
    if 'user_id' not in session:
        return redirect('/')
    user_diction ={
        'id':session['user_id']
    }
    return render_template('myplaces.html', user= User.get_by_id(user_diction), places = Place.get_all_places_by_user(user_diction))


@app.route("/viewplaces/<int:id>")
def view_place_page(id):
    if 'user_id' not in session:
        return redirect('/')
    place_diction = {
        'id':id  #this is the id of the place
    }
    user_diction ={
        'id':session['user_id']
    }
    return render_template('viewplaces.html', user= User.get_by_id(user_diction),place = Place.get_place_one_user(place_diction))
    

#deliver edit place html
@app.route("/place/edit/<int:id>")
def edit_place(id):
    if 'user_id' not in session:
        return redirect('/')
    place_diction = {
        'id':id 
    }
    user_diction ={
        'id':session['user_id']
    }
    return render_template('myplacedit.html', user = User.get_by_id(user_diction),place = Place.get_place_one_user(place_diction))
    
@app.route("/place/update/<int:id>", methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Place.validate_place(request.form):
        return redirect(f"/place/edit/{id}")
    place_diction = {
        'id': id, #the id from place (WHERE id =)
        'city': request.form['city'],
        'state': request.form['state'],
        'name':request.form['name'],
        'type': request.form['type'],
        'vibe': request.form['vibe'],
        'price': request.form['price'],
        'description': request.form['description'],
    }
    Place.update(place_diction)
    return redirect('/home')


@app.route("/places/goplaces")
def places_city():
    if 'user_id' not in session:
        return redirect('/')
    # if not Place.validate_place(request.form):
    #     return redirect(f"/place/edit/{id}")
    place_diction = {
        'city':request.args['city']
    }
    return render_template('placereview.html',places = Place.get_all_places_by_city(place_diction))


@app.route("/place/delete/<int:id>", methods = ['POST'])
def delete(id):
    Place.delete(request.form)
    return redirect('/home')




# API route
# @app.route("/insta/<int:id>")
# def get_insta(id):
#     if request.args['place']:
#         insta_pic = requests.get(f"https://instagram188.p.rapidapi.com/userphoto/instagram/{request.arg['place']}").json()
    
#     return render_template('viewplaces.html', results = insta_pic)
# pass













#ORIGINAL(DO NOT EDIT)
# @app.route('/myplaces/')
# def my_places():
#     if 'user_id' not in session:
#         return redirect('/')
#     user_diction ={
#         'id':session['user_id']
#     }
#     return render_template('myplaces.html', user= User.get_by_id(user_diction),place = Place.get_all_places_with_reviewers())