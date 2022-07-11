from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import requests
from flask_app.models import user

class Place:
    db_place = 'locals_only'
    def __init__(self,data):
        self.id  = data['id ']
        self.name = data['name']
        self.city = data['city']
        self.state= data['state']
        self.type = data['type']
        self.vibe = data['vibe']
        self.price = data['price']
        pass