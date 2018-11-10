# installed libs
from flask_restful import Resource

# local libs
from app.api.models.users import UserModel

# local variables
model = UserModel()

class Users(Resource):
    """Fetch all user with all details for each"""
    def get(self):
        """Fetch all users"""
        devs = model.get_all_users()
        return (
            {
                "message":"Our lovely users",
                "developers":devs
            }
        ), 200
