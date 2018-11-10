# installed libs
from werkzeug.exeptions import BadRequest, NotFound, Unauthorized

# local modules
from app.api.models.base_model import  MI, Meetup

class MeetupModel(object):
    """This is the meetup model for the meetups"""
    def get_all_meetups(self):
        """Fetch all meetups"""
        meetups = Meetup.query.filter().all()
        meetups_ = []
        if len(meetups) == 0:
            return (
                {
                    "messasge":"No meetups"
                }
            ), 200
        else:
            for i in meetups:
                # loop via all meetups and return dict
                meetup_data = {
                    "location":i.location,
                    "meetup_id":i.meetup_id,
                    "meetup_title":i.meetup_title,
                    "meetup_theme":i.meetup_theme,
                    "tags":i.tags,
                    "date":i.time,
                    "dev_limit":i.dev_limit
                }
                meetups_.append(meetups)
            return meetups_

    def create_meetup(self):
        """Create a meetup"""
        pass