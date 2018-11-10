# system libs
from uuid import uuid4
from datetime import datetime
import pdb

# installed libs
from werkzeug.exceptions import Unauthorized, NotFound, BadRequest

# local libs
from app.api.models.base_model import C2B, Bits, C2C
from app.api.models.bits import BitModel
from app.api.models.profile import ProfileModel

# local vars
b = BitModel()
p = ProfileModel()

class CommentModel(object):
    """This is the comments model"""
    def __init__(self):
        """define the constructor"""
        pass

    def add_comment(self, bit, bit_comment):
        """add a comment to a bit"""
        bit_data = b.get_one_bit(bit)
        comment = C2B(
            comment_id=str(uuid4()),
            bit_title = bit_data['bit_title'],
            comment = bit_comment,
            bit_author = p.get_name_by_token().username,
            timestamp=str(datetime.utcnow())
        )
        comment.save()
        return bit

    def add_c2c(self, comment_id, the_comment):
        """add a comment to comment existing"""
        comment = C2B.query.filter(C2B.comment_id == comment_id).first()
        other_comments = C2C.query.filter(C2C.child_comment_id == comment_id).first()
        if comment or other_comments:
            new_comment = C2C(
                child_comment_id = str(uuid4()),
                parent_comment_id = comment_id,
                author = p.get_name_by_token().username,
                comment = the_comment,
                timestamp = str(datetime.utcnow())
            )
            new_comment.save()
            return the_comment
        else:
            raise NotFound("That comment does not exist in the database")
    
    def delete_comment(self, comment_id):
        """delete a comment"""
        comment = C2B.query.filter(C2B.comment_id == comment_id).first()
        other_comments = C2C.query.filter(
            C2C.child_comment_id == comment_id).first()
        if comment:
            if p.get_name_by_token().username == comment.bit_author:
                comment.remove()
            else:
                raise Unauthorized("You cannot delete another developers comment")
        elif other_comments:
            if p.get_name_by_token().username == other_comments.author:
                other_comments.remove()
            else:
                raise Unauthorized("You cannot delete another developers comment")
        else:
            raise NotFound("No comment of that Id exists in the database")

    def update_comment(self, comment_id, comment_msg):
        """update own comment"""
        comment = C2B.query.filter(C2B.comment_id == comment_id).first()
        comment_ = C2C.query.filter(
            C2C.child_comment_id == comment_id
        ).first()
        if comment:
            if p.get_name_by_token().username == comment.bit_author:
                comment.comment = comment_msg
                comment.save()
            else:
                raise Unauthorized("You cannot edit an existing comment made by another dev")
        elif comment_:
            if p.get_name_by_token().username == comment_.author:
                comment_.comment = comment_msg
                comment_.save()
            else:
                raise Unauthorized("You cannot edit an existing comment made by another dev")  