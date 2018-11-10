# installed libs
from flask_restful import Resource, reqparse

# local libs
from app.api.models.pots import PotModel
from app.api.pro import auth_required
from app.api.models.notifications import NotificationModel as n

# local vars
model = PotModel()

class Pots(Resource):
    """Pots resource"""
    @auth_required
    def post(self, username):
        """Be a pot"""
        msg = model.become_a_pot(username)
        n().save_notification("You have just potted {}".format(username))
        return (
            {
                "message":"{}".format(msg)
            }
        ), 201