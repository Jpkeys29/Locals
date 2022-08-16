from sqlite3 import Row
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import pprint

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = 'locals'
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.places =[] # empty list holding places for this user

    @classmethod
    def create(cls,data):
        query = 'insert into users(first_name,last_name,email,password) VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s);'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @staticmethod
    def validate_user(form_data):
        valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,form_data)
        if len(results)>0:
            flash("Email already taken")
            valid = False
        if len(form_data['first_name'])<2:
            flash("Name must be at least two characters")
            valid = False 
        if len(form_data['last_name'])<2:
            flash("Last name must be at least two characters")
            valid = False 
        if form_data['password'] != form_data['confirm']:
            flash("Passwords need to match")
            valid = False
        if len(form_data['password'])< 8:
            valid = False
            flash('Password must be at least 8 characters long')
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Please enter valid email address")
            valid = False
        return valid
    
    @classmethod
    def get_by_id(cls,data):
        query = 'select * from users where id = %(id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) ==0:   #to check if the user is in the db
            return False
        if len(results)>=1:
            valid = False
        return cls(results[0])

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db_name).query_db(query)
        # pprint.pprint(results)
        all_users = []
        for row in results:
            all_users.append(cls(row))
        # print(row)
        return all_users
        print(all_users)

    @classmethod
    def get_one_user_with_places(cls,data):
        query = "SELECT * FROM users LEFT JOIN places ON users.id = user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)  #list of dictionaries
        print(f"RESULTS:{results}")
        #make an user object
        this_user = cls(results[0])
        #go through each place
        for row in results:
        # make a dictionary for the place info
            place_info ={
                'id': row['place.id'],
                'city':row['city'],
                'state':row['state'],
                'name':row['name'],
                'type':row['type'],
                'vibe':row['vibe'],
                'price':row['price'],
                'description':row['description'],
                'created_at':row['place.created_at'],
                'uptdated_at':row['place.uptdated_at'],
            }
        

        pass