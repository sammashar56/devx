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

class PotModel(object):
    """Pots and poting model"""
    def __init__(self):
        pass

    def become_a_pot(self, dev_name):
        """Become a pot to another by poting"""
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''
        if auth_token:
            response = t.decode_auth_token(auth_token)
            if isinstance(response, str):
                developer = model.get_user(response)
                print(developer['coder_name'])
                if not developer:
                    raise Unauthorized("You need to login in order to pot someone")
                else:
                    dev = Dev.query.filter(Dev.username == dev_name).first()
                    if dev:
                        potter = Pot.query.filter(
                            Pot.the_potter == developer['coder_name'] and Pot.the_potted == dev.username
                        ).first()
                        if potter:
                            if potter.the_potter != developer['coder_name']:
                                potter.remove()
                                return "You have unpotted '{}'".format(dev.username)
                            else:
                                raise BadRequest("You cannot unpot yourself")
                        elif developer['coder_name'] == dev.username:
                            raise Unauthorized("You cannot pot your self")
                        elif developer['coder_name'] != dev.username:
                            pot = Pot(the_potter=developer['coder_name'], the_potted=dev.username)
                            pot.save()
                            return "You have just potted {}".format(dev.username)
                        else:
                            return "You are trying something that is not allowed"
                    else:
                        raise NotFound("The developer does not exist")
            else:
                raise Unauthorized("We cannot seem to identify can you try logging in again")
        else:
            raise Unauthorized("We cannot seem to identify can you try logging in again")