from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import requests
from flask_app.models import user

class Place:
    db_place = 'locals_only'
    def __init__(self,data):
        self.id  = data['id ']
        self.city = data['city']
        self.state= data['state']
        self.name = data['name']
        self.type = data['type']
        self.vibe = data['vibe']
        self.price = data['price']
        self.description = data['description']
        
    @classmethod
    def create_place(cls,data):
        query = "INSERT INTO places(city,state,name,type,vibe,price,description) VALUES (%(city)s,%(state)s,%(name)s,%(type)s,%(vibe)s,%(price)s,%(description)s);"
        results = connectToMySQL(cls.db_place).query_db(query,data)
        return results

    
