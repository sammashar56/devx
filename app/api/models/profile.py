# installed libs
from flask import request
from werkzeug.exceptions import Unauthorized, NotFound, BadRequest

# local imports 
from app.api.models.base_model import Dev, Pot
from app.api.token import Token
from app.api.models.auth import AuthModel

# local vars
t = Token()
model = AuthModel()

# The profile model containing method to get user details
class ProfileModel(object):
    """This is the profile model"""
    def get_name_by_token(self):
        """Get username from token"""
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ' '
        if auth_token:
            username = t.decode_auth_token(auth_token)
            dev = Dev.query.filter(Dev.username == username).first()
            if dev:
                return dev
            else:
                raise Unauthorized("Please login to continue")
        else:
            raise Unauthorized("Please login to continue")
    
    def get_acc(self):
        """Get user account details"""
        username = self.get_name_by_token().username
        acc_details = model.get_user(username)
        return acc_details

    def get_potters(self):
        """Get how many potters a developer has"""
        pots = Pot.query.filter(Pot.the_potted == self.get_acc()['coder_name']).all()
        return len(pots)

    def get_potted(self):
        """Get how many pottings made by a dev"""
        pottings = Pot.query.filter(Pot.the_potter == self.get_acc()['coder_name']).all()
        return len(pottings)

    def get_account(self, username):
        """Get user account with details"""
        acc_details = model.get_user(username)
        return acc_details

    def the_potted(self, username):
        """Fecth counts of users being potted"""
        pots = Pot.query.filter(Pot.the_potted == username).all()
        return len(pots)

    def the_potters(self, username):
        """Fecth counts of users potting"""
        pots = Pot.query.filter(Pot.the_potter == username).all()
        return len(pots)