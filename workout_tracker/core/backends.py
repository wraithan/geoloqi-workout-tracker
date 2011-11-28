from django.conf import settings
from django.contrib.auth.models import User

from core import GEOLOQI_TOKEN_URI, oauth2_token
from core.models import GeoloqiProfile


class OAuth2Backend(object):
    def authenticate(self, code=None):
        if code is None:
            return None
        else:
            auth_stuff = oauth2_token(GEOLOQI_TOKEN_URI,
                                      settings.GEOLOQI_CLIENT_ID,
                                      settings.GEOLOQI_CLIENT_SECRET,
                                      code,
                                      settings.GEOLOQI_REDIRECT_URI)

            user = User.objects.filter(geoloqiprofile__oauth_user_id=auth_stuff['user_id'])
            if user.exists():
                user = user.get()
            else:
                user = User.objects.create(username=auth_stuff['username'],
                                           first_name=auth_stuff['display_name'],
                                           is_active=True, email='')
                GeoloqiProfile.objects.create(user=user,
                                              oauth_user_id=auth_stuff['user_id'],
                                              access_token=auth_stuff['access_token'],
                                              refresh_token=auth_stuff['refresh_token'])

        return user
        
        
        
