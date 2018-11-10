# installed libs
from flask_restful import Resource, reqparse

# local libs
from app.api.pro import auth_required as protection
from app.api.models.notifications import NotificationModel as n

class Notification(Resource):
    """This is the class holding the notifications endpoints"""
    # protect this route
    @protection
    def get(self):
        """Fetch all notifications made"""
        notifications = n().get_notifications()
        if len(notifications) == 0:
            return (
                {
                    "message":"No notifications"
                }
            ), 200
        else:
            return (
                {
                    "notifications":notifications
                }
            ), 200

    def delete(self):
        pass