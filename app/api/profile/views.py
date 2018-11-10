"""
This is the file containing the endpoint for a developer to view profile
details such as 
:potters - This are the number of potters poting the dev
:account_details - This are the account details
"""

# Installed libs
from flask_restful import Resource

# local modules
from app.api.models.profile import ProfileModel
from app.api.models.base_model import Pot
from app.api.pro import auth_required

# local variables
# assign the AuthModel object to a var
model = ProfileModel()

# Creation of the endpoint
class Profile(Resource):
    """This is the Resource for all profile endpoints
    :PUT to update the acc details
    :GET to get the profile details
    """
    @auth_required
    def get(self):
        """Get account details"""
        data = model.get_acc()
        potters = model.get_potters()
        pottings = model.get_potted()
        return (
            {
                "acc":data,
                "potters":potters,
                "potting":pottings
            }
        ), 200