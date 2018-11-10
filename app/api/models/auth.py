# Installed libs
from werkzeug.exceptions import Unauthorized, NotFound

# Local imports
from app.api.models.base_model import BaseModel, Dev, Blacklist

class AuthModel(BaseModel):
    def __init__(self):
        super().__init__()     

    def get_user(self, coder_name):
        """Get user details with name"""
        dev = Dev.query.filter(Dev.username == coder_name).first()
        if dev:
            data = {
                "coder_name":dev.username,
                "email":dev.email,
                "stack":dev.stack,
                "repo_link":dev.repo_link,
                "password":dev.password,
                "primary_language":dev.language
            }
            return data 
        else:
            raise NotFound("You dont have an account of that name")        
            

    def save_dev(self, data):
        if Dev.query.filter(Dev.email == data['email']).first():
            raise Unauthorized("I am afraid your email is already taken")
        elif Dev.query.filter(Dev.repo_link == data['repo_link']).first():
            raise Unauthorized("I am afraid your github or bitbucket is already in use")
        elif Dev.query.filter(Dev.username == data['username']).first():
            raise Unauthorized("I am afraid your coder name is already taken")
        else:
            dev = Dev(
                username = data['username'],
                email = data['email'],
                repo_link = data['repo_link'],
                language = data['language'],
                password = data['password'],
                bio = data['bio'],
                stack = data['stack'],
                portfolio = data['portfolio']
            )
            dev.save()
            return data

    def check_token(self, token):
        """Check if token exists"""
        if Blacklist.query.filter(Blacklist.token == token).first():
            return token
        else:
            return None
