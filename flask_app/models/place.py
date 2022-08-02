import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import user

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
        
    @classmethod
    def create_place(cls,data):
        query = "INSERT INTO places(city,state,name,type,vibe,price,description,user_id) VALUES (%(city)s,%(state)s,%(name)s,%(type)s,%(vibe)s,%(price)s,%(description)s,%(user_id)s);"
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
    def get_one_place(cls,data):
        query = "SELECT * FROM places WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_place).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    # @classmethod
    # def update(cls,data):
    #     query = UPDATE places SET 
    #     pass


