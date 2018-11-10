# local modules
from app.api.models.base_model import Dev
from app.api.models.auth import AuthModel
from app.api.models.profile import ProfileModel

# local vars 
auth_model = AuthModel()
p = ProfileModel()

class UserModel(object):
    """This is the user model"""
    def get_all_users(self):
        """Fetch all users with their details"""
        devs = Dev.query.filter().all()
        developers = []
        for i in devs:
            user_data = p.get_account(i.username)
            user_data['pots'] = p.the_potted(i.username)
            user_data['potting'] = p.the_potters(i.username)
            developers.append(user_data)
        
        return developers
