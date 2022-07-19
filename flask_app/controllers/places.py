

# @app.route('/place/create', methods=['POST'])
# def create_place():
#     if 'user_id' not in session:
#         return redirect('/')
#     place_diction = {
#         'city': request.form['city'],
#         'state': request.form['state'],
#         'type': request.form['type'],
#         'vibe': request.form['vibe'],
#         'price': request.form['price'],
#         'description': request.form['description'],
#     }
#     session['user_id']= Place.Create_place(place_diction)
#     return redirect (?????)