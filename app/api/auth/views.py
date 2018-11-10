from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

# Local imports
from app.api.models.auth import AuthModel
from app.api.validators import Validate
from app.api.auth.checkers import languages
from app.api.token import Token

# Local vars
v = Validate()
model = AuthModel()
t = Token()

class Registration(Resource):
    """Dev registration"""
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "coder_name",
            type=str,
            required=True,
            help="Please provide a coder name"
        )
        parser.add_argument(
            "coder_primary_language",
            type=str,
            required=True,
            help="Please provide your primary_laguage"
        )
        parser.add_argument(
            "profile_link",
            type=str,
            required=True,
            help="Please provide a repo be it bitbucket or github"
        )
        parser.add_argument(
            "coder_bio",
            type=str            
        )
        parser.add_argument(
            "coder_portfolio",
            type=str
        )
        parser.add_argument(
            "coder_stack",
            type=str,
            required=True,
            help="Provide a stack for a better experience"
        )
        parser.add_argument(
            "coder_email",
            type=str,
            required=True,
            help="Provide a valid email i.e. *******.*****@*****.**** or ****@****.***"
        )
        parser.add_argument(
            "coder_password",
            type=str,
            required=True,
            help="Provide a password more than six characters"
        )
        parser.add_argument(
            "confirm_password",
            type=str,
            required=True,
            help="Please confirm your password"
        )
        args = parser.parse_args()
        email = v.check_email(args['coder_email'])
        coder_name = v.check_name(args['coder_name'])
        if args['confirm_password'] == args['coder_password']:
            password = v.check_password(args['coder_password'])
        else:
            raise BadRequest("The passwords do not match")
        profile_link = v.check_repo_link(args['profile_link'])
        if args['coder_primary_language'] not in languages:
            raise BadRequest("The laguage you provided is not added yet but we will soon add a few more for all developers to be welcomed")
        else:
            language = args['coder_primary_language']

        dev_data = {
            "username":coder_name,
            "email":email,
            "repo_link":profile_link,
            "language":language,
            "password":generate_password_hash(password),
            "bio":args['coder_bio'],
            "stack":args['coder_stack'],
            "portfolio":args['coder_portfolio']
        }
        data = model.save_dev(dev_data)        
        return ({"message":"Account created, your devx id is {}"
        .format(dev_data['username']), "details":data}), 201

class Login(Resource):
    """Login the developer resource"""
    def post(self):
        """Login a developer"""
        parser = reqparse.RequestParser()
        parser.add_argument(
            'devx_id',
            type=str,
            required=True,
            help="Please provide your devX id"
        )
        parser.add_argument(
            'password',
            type=str,
            required=True,
            help="Please provide a password for your account"
        )
        args = parser.parse_args()
        password = v.check_password(args['password'])
        data = model.get_user(args['devx_id'])
        if check_password_hash(data['password'], password):
            token = t.encode_auth_token(data['coder_name'])
            return (
                {
                    "message":"Logged in successfully",
                    "developer_data":data,
                    "token":token.decode()
                }
            ), 200
        else:
            return (
                {
                    "message":"Passwords do not match"
                }
            ), 401

        
