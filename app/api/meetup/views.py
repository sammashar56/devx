# installed libs
from flask_restful import Resource, reqparse

# local libs
# ...

class Meetup(Resource):
    """This are the meetup endpoints"""
    def get(self):
        """Fetch all meetups"""
        pass

    def post(self):
        """Create a meetup"""
        pass

class SingleMeetup(Resource):
    """This are the endpoints for single meetups"""
    def put(self):
        """Update meetup details"""
        pass

    def delete(self):
        """Delete a meetup"""
        pass