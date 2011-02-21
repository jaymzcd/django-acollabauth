from django.conf import settings
from django.contrib.auth.models import User
import urllib

class ActiveCollabBackend(object):
    """ Logs into a given Active Collab site and creates
    a new user based on a successful login there """

    supports_object_permissions = False
    supports_inactive_user = False
    supports_anonymous_user = False

    def __init__(self):
        self.login_url = settings.AC_URL + '/login'

    def authenticate(self, username=None, password=None):
        try:
            # turn jaymz@u-dox.com into just jaymz
            email_user = username[:username.index('@')]
        except ValueError:
            # AC uses emails to login, so can fail now
            return None

        # Pass in the form data to our AC url
        data = {
            'login[email]': username,
            'login[password]': password,
            'login[remember]': 1,
            'submitted': 'submitted',
        }
        response = urllib.urlopen(self.login_url, urllib.urlencode(data))
        if 're_route=dashboard' in response.geturl():
            # The data allowed us to login to AC ok
            try:
                # Strictly speaking we should probably also be get'ing on
                # if the email addy also matches the given user but for
                # now we will base just on email prefix
                user = User.objects.get(username=email_user)
            except User.DoesNotExist:
                user = User(username=email_user, email=username)
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
