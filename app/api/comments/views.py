# system libs
from datetime import datetime as dt

# installed libs
from flask_restful import Resource, reqparse

# local module 
from app.api.models.comments import CommentModel
from app.api.pro import auth_required
from app.api.models.notifications import NotificationModel as n

# local vars 
model = CommentModel()

class BitComment(Resource):
    """Comment on a bit"""
    @auth_required
    def post(self, bit_title):
        """Comment on a bit"""
        parser = reqparse.RequestParser()
        parser.add_argument(
            'comment',
            type=str, 
            required=True,
            help='What do you think about this bit'
        )
        args = parser.parse_args()
        data = model.add_comment(bit_title, args['comment'])
        n().save_notification("You have commented on a bit of title #{}".format(bit_title))
        return (
            {
                "message":"comment has been saved",
                "bit_title":data
            }
        ), 201

class C2Cs(Resource):
    """Comment on a comment"""
    @auth_required
    def post(self, comment_id):
        """Comment on a comment"""
        parser = reqparse.RequestParser()
        parser.add_argument(
            'comment',
            type=str, 
            required=True,
            help = "What do you think about this comment"
        )
        args = parser.parse_args()
        data = model.add_c2c(comment_id, args['comment'])
        n().save_notification("You have commented on a comment at {}".format(dt.utcnow()))
        return (
            {
                "message":"comment has been saved",
                "comment":data
            }
        ), 201

class Comments(Resource):
    """Endpoints involving all comments"""
    @auth_required
    def delete(self, comment_id):
        """Delete a specific comment"""
        model.delete_comment(comment_id)
        return (
            {
                "message":"Successfull deletion"
            }
        ), 204

    @auth_required
    def put(self, comment_id):
        """Update a comment"""
        parser = reqparse.RequestParser()
        parser.add_argument(
            'comment',
            type=str, 
            required=True,
            help='Perfection is good, give the comment'
        )
        args = parser.parse_args()
        model.update_comment(comment_id, args['comment'])
        
        return (
            {
                "message":"Comment was updated"
            }
        ), 201