from functools import wraps
import os

from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
import jwt

from app.api.models.auth import AuthModel
from app.api.token import Token

t = Token()
model = AuthModel()

def auth_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''
        if auth_token:
            response = t.decode_auth_token(auth_token)
            if isinstance(response, str):
                user_credentials = model.get_user(response)
                print(user_credentials)
                if not user_credentials:
                    raise Unauthorized("You need to signup or login")
                return function(*args, **kwargs)
            else:
                raise Unauthorized("Please login")
        else:
            raise Unauthorized("It seems you are not logged in")
    return decorated
