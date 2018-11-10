import re

from werkzeug.exceptions import BadRequest

class Validate(object):
    """Validation of certain queries"""
    def __init__(self):
        pass

    def check_repo_link(self, link):
        """Check github link"""
        if not re.search('https://github.com/', link):
            if not re.search('https://bitbucket.com/', link):
                raise BadRequest("The profile link is neither a github or bitbucket valid link")
            else:
                return link
        return link

    def check_email(self, email):
        """ Check email validity """
        if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
            email):
                raise BadRequest("Please provide a valid email")
        return email

    def check_password(self, password):
        """Check password link"""
        if len(password) < 6:
            raise BadRequest("Password should be a minimum of six characters")
        elif len(password) > 25:
            raise BadRequest("Password should be a minimum of thirty two characters")
        else:
            return password

    def check_name(self, name):
        """Check username valid"""
        if len(name) < 3:
            raise BadRequest("Coder name is too short please")
        elif re.search('[$,%,@,&,*,!]', name):
            raise BadRequest("Coder name should not contain a special character")
        else:
            return name

    
            
            
