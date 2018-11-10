import os

# Installed libs
from flask import Flask
from flask_mongoalchemy import MongoAlchemy


app = Flask(__name__)
# app.config['MONGO_DBNAME'] = os.getenv("MONGO_DBNAME")
# app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['MONGOALCHEMY_DATABASE'] = os.getenv("MONGO_DBNAME")
app.config['MONGOALCHEMY_CONNECTION_STRING' ] = os.getenv("MONGO_URI")

mongo = MongoAlchemy(app)

class BaseModel(object):
    def __init__(self):
        self.mongo = mongo

class Pot(mongo.Document):
    """Document holding all pots made in devx"""
    the_potter = mongo.StringField()
    the_potted = mongo.StringField()

class Dev(mongo.Document):
    """create a mongo document"""
    username = mongo.StringField()
    email = mongo.StringField()
    repo_link = mongo.StringField()
    language = mongo.StringField()
    password = mongo.StringField()
    bio = mongo.StringField()
    stack = mongo.StringField()
    portfolio = mongo.StringField(required=False)

class Blacklist(mongo.Document):
    """create a token mongo document"""
    token = mongo.StringField()

class C2B(mongo.Document):
    """create a comment mongo document"""
    comment_id = mongo.StringField()
    bit_title = mongo.StringField()
    comment =  mongo.StringField()
    bit_author = mongo.StringField()
    timestamp = mongo.StringField()

class C2C(mongo.Document):
    """create a comments to comments document"""
    child_comment_id = mongo.StringField()
    parent_comment_id = mongo.StringField()
    author = mongo.StringField()
    comment = mongo.StringField()
    timestamp = mongo.StringField()

class Bits(mongo.Document):
    """create a bits mongo document"""
    bit_title = mongo.StringField()
    bit_msg = mongo.StringField()
    bit_author = mongo.StringField()
    timestamp = mongo.StringField()

class Notifications(mongo.Document):
    """create a notification database"""
    not_id = mongo.StringField()
    developer = mongo.StringField()
    not_msg = mongo.StringField()
    timestamp = mongo.StringField()

class MI(mongo.Document):
    """create meetup invites document"""
    dev = mongo.StringField()
    meetup_id = mongo.StringField()
    status = mongo.BoolField()

class Meetup(mongo.Document):
    """This is the meetup document"""
    location = mongo.StringField()
    meetup_id = mongo.StringField()
    meetup_title = mongo.StringField()
    meetup_theme = mongo.StringField()
    tags = mongo.AnythingField()
    time = mongo.StringField()
    dev_limit = mongo.IntField()