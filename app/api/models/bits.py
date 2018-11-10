# installed libs
from flask import request
from werkzeug.exceptions import Unauthorized, NotFound, BadRequest

# local imports 
from app.api.models.base_model import Dev, Bits
from app.api.token import Token
from app.api.models.auth import AuthModel
from app.api.models.profile import ProfileModel

# local vars
t = Token()
a = AuthModel()
p = ProfileModel()

class BitModel(object):
    """This is the bit model"""
    def __init__(self):
        """define the constructor"""
        pass

    def check_bit_title_used(self, bit_title):
        """Check if a bit already has that title"""
        bit = Bits.query.filter(Bits.bit_title == bit_title.replace(" ", "")).first()
        if bit:
            raise BadRequest("A bit holds that title as a message")
        else:
            return bit_title

    def add_bit(self, data):
        """Add a bit to the database"""
        bit_title = self.check_bit_title_used(data['bit_title'])
        author = p.get_name_by_token()
        bit = Bits(
            bit_title = bit_title.replace(" ", ""),
            bit_msg = data['bit_msg'],
            bit_author = author.username,
            timestamp = str(data['timestamp'])
        )
        bit.save()
        return data

    def get_all_bits(self):
        """Fetch all bits made by the user"""
        bits = Bits.query.filter().all()
        _bits = []
        for i in bits:
            _bit_data = {
                "bit_title":i.bit_title,
                "bit_msg":i.bit_msg,
                "bit_author":i.bit_author,
                "bit_creation":i.timestamp
            }
            _bits.append(_bit_data)
        return _bits

    def get_one_bit(self, bit_title):
        """Fetch one bit by title"""
        bit = Bits.query.filter(Bits.bit_title == bit_title).first()
        if bit:
            bit_data = {
                "bit_title":bit.bit_title,
                "bit_msg":bit.bit_msg,
                "bit_author":bit.bit_author,
                "timestamp":bit.timestamp
            }
            return bit_data
        else:
            raise NotFound("No bit of that name exists")

    def update_bit(self, bit_title, bit_msg):
        """Update a bit msg"""
        author = p.get_name_by_token()
        bit = Bits.query.filter(Bits.bit_title == bit_title).first()
        if bit:
            if bit.bit_author == author.username: 
                bit.bit_msg = bit_msg
                bit.save()
                return bit_title
            else:
                raise Unauthorized("You cannot delete a bit from another developer")
        else:
            raise NotFound("No bit of that name exists")

    def delete_bit(self, bit_title):
        """Delete a bit"""
        bit = Bits.query.filter(Bits.bit_title == bit_title).first()
        if bit:
            if bit.bit_author == p.get_name_by_token():
                bit.remove()
                return 
            else:
                raise Unauthorized("You cannot delete a bit from another developer")
        else:
            raise NotFound("No bit of that name exists")