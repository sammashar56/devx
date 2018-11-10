# system libs
import datetime as dt

# installed libs
from flask_restful import Resource, reqparse 

# local modules
from app.api.pro import auth_required
from app.api.models.bits import BitModel
from app.api.models.notifications import NotificationModel as n

# local vars
model = BitModel()

class Bits(Resource):
    """Bit endpoint class resource"""
    @auth_required
    def post(self):
        """Create a bit"""
        parser = reqparse.RequestParser()
        parser.add_argument(
            'bit_title',
            type=str,
            required=True,
            help='Provide a unique bit title'
        )
        parser.add_argument(
            'bit_msg',
            type=str,
            required=True,
            help='Provide the bit message'
        )
        args = parser.parse_args()

        data = {
            "bit_title":args['bit_title'].lower(),
            "bit_msg":args['bit_msg'],
            "timestamp":str(dt.datetime.utcnow())
        }
        return_data = model.add_bit(data)
        n().save_notification("You added bit of title #{}".format(data['bit_title']))
        return (
            {
                "status":"Success",
                "message":"A bit added",
                "bit_data":return_data
            }
        ), 201

    def get(self):
        """Fetch all bits"""
        bits = model.get_all_bits()
        if len(bits) == 0:
            return (
                {
                    "message":"No bits made yet"
                }
            ), 200
        return  (
            {
                "bits":bits
            }
        ), 200

class EachBit(Resource):
    """CRUD each specific bit with title"""
    @auth_required
    def get(self, bit_title):
        """Fetch a specific bit by title"""
        bit_data = model.get_one_bit(bit_title)
        return (
            {
                "bit_data":bit_data
            }
        ), 200

    @auth_required
    def put(self, bit_title):
        """Update a bit title"""
        parser = reqparse.RequestParser()
        parser.add_argument(
            "bit_msg",
            type=str,
            required=True, 
            help="Enter a message to update the bit msg"
        )
        args = parser.parse_args()
        bit_title_returned = model.update_bit(bit_title, args['bit_msg'])
        n().save_notification("You have edited a bit of title {}".format(bit_title_returned))
        return (
            {
                "message":"Bit successfully updated",
                "bit_title":bit_title_returned
            }
        ), 201

    @auth_required
    def delete(self, bit_title):
        """Delete a bit """
        bit_title_returned = model.delete_bit(bit_title)
        n().save_notification("You deleted a bit of title {}".format(bit_title))
        return (
            {
                "message":"Delete a specific bit",
                "bit_title":bit_title_returned
            }
        ), 204