import json
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session,request,flash
from flask_app.models import user
from pprint import pprint
# import requests

class Place:
    db_place = 'locals'
    def __init__(self,data):
        self.id  = data['id']
        self.city = data['city']
        self.state= data['state']
        self.name = data['name']
        self.type = data['type']
        self.vibe = data['vibe']
        self.price = data['price']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id'] #It tells us which user created that place
        self.reviewer = None #Link a user to this place
        
    @classmethod
    def create_place(cls,data):
        query = "INSERT INTO places (city,state,name,type,vibe,price,description,user_id) VALUES (%(city)s,%(state)s,%(name)s,%(type)s,%(vibe)s,%(price)s,%(description)s,%(user_id)s);"
        return connectToMySQL(cls.db_place).query_db(query,data)
        

    @classmethod
    def get_all_places(cls):
        query = 'SELECT * FROM places;'
        results = connectToMySQL(cls.db_place).query_db(query)
        places_objects = []
        for row in results:
            places_objects.append(cls(row))
        return places_objects
        

    @classmethod
    def get_all_places_by_city(cls,data):
        query = "SELECT * FROM places WHERE city = %(city)s;"
        results = connectToMySQL(cls.db_place).query_db(query,data)
        # pprint(results)
        if len(results)<1:
            return "AWWW there are no places for this city"
        all_places_by_city = []
        for row in results:           
            all_places_by_city.append(cls(row))
        return all_places_by_city

    @classmethod
    def get_one_place(cls,data):
        query = "SELECT * FROM places WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_place).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_place(form_data):
        valid = True
        if len(form_data["city"])<2:
            valid = False
            flash('Location must be at least 2 characters')
        if len(form_data["name"])<2:
            valid = False
            flash('The name of the place must be at least 2 characters')
        if len(form_data["description"])<3:
            valid = False
            flash('Description must be at least 3 characters')
        return valid

    @classmethod
    def get_all_places_with_reviewers(cls):
        query = "SELECT * FROM places JOIN users ON places.user_id = users.id"
        results = connectToMySQL(cls.db_place).query_db(query)
        # pprint(results)
        all_places = []
        for row in results:
            one_place_object = cls(row)

            one_place_user_dict ={
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at'],
            }
        
            this_reviewer = user.User(one_place_user_dict) 
            one_place_object.reviewer = this_reviewer 
            all_places.append(one_place_object)
        return all_places


    @classmethod
    def get_place_one_user(cls,data):
        query = "SELECT * FROM places JOIN users ON places.user_id = users.id WHERE places.id =%(id)s;"
        results = connectToMySQL(cls.db_place).query_db(query,data)
        place_object = cls(results[0]) # 'place_object' represents a dictionary at index 0 in the list called "results"
        user_diction_object ={
            'id': results[0]['users.id'],
            'first_name': results [0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at'],
        }
        this_user_object = user.User(user_diction_object)
        place_object.reviewer = this_user_object
        return place_object

    @classmethod
    def get_all_places_by_user(cls,data):
        query = "SELECT * FROM places JOIN users ON places.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_place).query_db(query,data)
        all_places = []
        for row in results:
            this_place = cls(row)
            user_dictionary = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"],
            }
            this_reviewer = user.User(user_dictionary)
            this_place.reviewer = this_reviewer
            all_places.append(this_place)
        return all_places

    @classmethod
    def update(cls,data):
        query = "UPDATE places SET city=%(city)s, state=%(state)s, name=%(name)s, type=%(type)s, vibe=%(vibe)s, price=%(price)s, description=%(description)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db_place).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM places WHERE id = %(id)s;"
        return connectToMySQL(cls.db_place).query_db(query,data)



    # @staticmethod
    # def api_call(request):
    #     url = "https://instagram188.p.rapidapi.com/userphoto/instagram"

    #     headers = {
    #         "X-RapidAPI-Key": "88e3695b8bmsh42ce67b8bf7a723p1d4abcjsn862b3172e524",
    #         "X-RapidAPI-Host": "instagram188.p.rapidapi.com"
    #     }

    #     response = requests.request("GET", url, headers=headers)

    #     profile_pics = response.json()

    #     pass
