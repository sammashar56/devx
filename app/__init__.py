# System libraries
import os

# Installed libraries
from flask import Flask
from flask_restful import Api
from werkzeug.contrib.fixers import ProxyFix
from flask_mongoalchemy import MongoAlchemy

# Local imports
from app.config import app_config
from app.api.auth.views import Registration, Login
from app.api.pots.views import Pots
from app.api.profile.views import Profile
from app.api.users.views import Users
from app.api.bits.views import Bits, EachBit
from app.api.comments.views import BitComment, C2Cs, Comments
from app.api.notifications.views import Notification

def create_app(configuration):
    # Initialize flask application
    app = Flask(__name__)

    # Setup the application configs
    app.url_map.strict_slashes = False
    print(configuration)
    app.config.from_object(app_config[configuration])
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_pyfile('config.py')

    # Initialize the flask api
    api = Api(app)

    # Set the mongo db uris and db name
    app.config['MONGOALCHEMY_DATABASE'] = os.getenv("MONGO_DBNAME")
    app.config['MONGOALCHEMY_CONNECTION_STRING' ] = os.getenv("MONGO_URI")

    # Initialize database
    db = MongoAlchemy(app)

    # Set the api endpoints
    api.add_resource(Registration, '/api/dev/up')
    api.add_resource(Login, '/api/dev/in')
    api.add_resource(Pots, '/api/dev/pot/<string:username>')
    api.add_resource(Profile, '/api/dev/profile')
    api.add_resource(Users, '/api/devs')
    api.add_resource(Bits, '/api/bits')
    api.add_resource(EachBit, '/api/bit/<string:bit_title>')
    api.add_resource(BitComment, '/api/bit/comment/<string:bit_title>')
    api.add_resource(C2Cs, '/api/comment/<string:comment_id>')
    api.add_resource(Comments, '/api/comments/<string:comment_id>')
    api.add_resource(Notification, '/api/dev/alerts')
    return {"app":app, "mongo":db}

