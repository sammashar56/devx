# system lib
import os
import datetime as dt

# installed libs
import jwt
from werkzeug.exceptions import Unauthorized, Forbidden

# local libs
from app.api.models.auth import AuthModel as auth

class Token(object):
    """All related token"""
    def encode_auth_token(self, coder_name):
        """generate auth token"""
        payload = {
            "exp":dt.datetime.utcnow() + dt.timedelta(minutes=1440),
            "iat":dt.datetime.utcnow(),
            "sub":coder_name
        }
        return jwt.encode(
            payload,
            os.getenv("SECRET_KEY"),
            algorithm='HS256'
        )

    def decode_auth_token(self, token):
        """decode auth token"""
        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"))
            is_blacklisted_token = auth().check_token(token)
        except jwt.ExpiredSignatureError:
            raise Unauthorized('Token has expired please login to authenticate')
        except jwt.InvalidTokenError:
            raise Unauthorized('You authorization token is invalid')
        if is_blacklisted_token:
            raise Unauthorized('You logout with this token try again')
        return payload['sub']
            