
import json
from rest.api.db import db
from sqlalchemy import Text,DateTime


class User(db.Model):
    # Columns
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, index=True)
    
    def __init__(self, username):
        self.username = username


class Image(db.Model):
    # Colunms
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    imagepath = db.Column(db.String(128),unique = True,index = True)
    feature = db.Column(Text)

    def dumps(self,arr):
        return json.dumps(arr)
    
    def loads(self,tmp_feature):
        return json.loads(tmp_feature)
    


class Log(db.Model):
    # Columns
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key = True ,autoincrement = True)
    username = db.Column(db.String(64), unique = True , index = True)
    imageres = db.Column(db.String(128), unique = True , index = True)
    datetime = db.Column(DateTime)
    type = db.Column(db.String(64))
