import json
from urllib import quote
from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from core.models import GeoLoqiProfile
import requests


GEOLOQI_AUTH_URI = 'https://geoloqi.com/oauth/authorize'
GEOLOQI_TOKEN_URI = 'https://api.geoloqi.com/1/oauth/token'

DAILYMILE_AUTH_URI = 'https://api.dailymile.com/oauth/authorize'
DAILYMILE_TOKEN_URI = 'https://api.dailymile.com/oauth/token'

def register(request):
    auth_url = '%(auth_uri)s?redirect_uri=%(redirect_uri)s&response_type=code&client_id=%(client_id)s' % {'auth_uri': GEOLOQI_AUTH_URI,
                                                                                                          'client_id': quote(settings.GEOLOQI_CLIENT_ID),
                                                                                                          'redirect_uri': quote(settings.GEOLOQI_REDIRECT_URI)}
    return HttpResponseRedirect(auth_url)


@render_to('core/success.html')
def register_callback(request):
    payload = {
        'grant_type': 'authorization_code',
        'client_id': settings.GEOLOQI_CLIENT_ID,
        'client_secret': settings.GEOLOQI_CLIENT_SECRET,
        'code': request.GET['code'],
        'redirect_uri': settings.GEOLOQI_REDIRECT_URI,
        }
    response = requests.post(GEOLOQI_TOKEN_URI, data=payload)
    auth_stuff = json.loads(response.content)
    user = User.objects.filter(geoloqiprofile__oauth_user_id=auth_stuff['user_id'])
    if user.exists():
        user = user.get()
    else:
        user = User.objects.create(username=auth_stuff['username'], first_name=auth_stuff['display_name'], is_active=True, email='')
        GeoLoqiProfile.objects.create(user=user,
                                      oauth_user_id=auth_stuff['user_id'],
                                      access_token=auth_stuff['access_token'],
                                      refresh_token=auth_stuff['refresh_token'])
    login(request, user)
    return locals()
