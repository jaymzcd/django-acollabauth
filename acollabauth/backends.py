from django.conf import settings
import urllib

class ActiveCollabBackend(object):
    """ Logs into a given Active Collab site and creates
    a new user based on a successful login there """

    def __init__(self):
        self.login_url = settings.AC_URL + '/login'

    def authenticate(self, username=None, password=None):
        pass

    def get_user(self, user_id):
        pass

