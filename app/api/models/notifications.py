# system libs
from datetime import datetime as dt
from uuid import uuid4
import pdb

# local modules
from app.api.models.base_model import Notifications as n
from app.api.models.profile import ProfileModel as p

class NotificationModel(object):
    """this is the notification model"""
    def __init__(self):
        """Define the constructor"""
        pass

    def save_notification(self, not_msg):
        """Save a notification"""
        dev = p().get_name_by_token()
        not_ = n(
            not_id=str(uuid4()),
            developer = dev.username,
            not_msg = not_msg,
            timestamp=str(dt.utcnow())
        )
        not_.save()

    def get_notifications(self):
        """Fetch all notifications"""
        developer = p().get_name_by_token()
        not_ = n.query.filter(n.developer == developer.username).all()
        notifications = []
        for i in not_:
            not_data = {
                "not_id":i.not_id,
                "notification":i.not_msg,
                "timestamp":i.timestamp
            }
            notifications.append(not_data)
        return notifications

        