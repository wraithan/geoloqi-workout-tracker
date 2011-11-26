import json
from urllib import quote
from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from core.models import GeoloqiProfile, DailyMileProfile
import requests


GEOLOQI_AUTH_URI = 'https://geoloqi.com/oauth/authorize'
GEOLOQI_TOKEN_URI = 'https://api.geoloqi.com/1/oauth/token'

DAILYMILE_AUTH_URI = 'https://api.dailymile.com/oauth/authorize'
DAILYMILE_TOKEN_URI = 'https://api.dailymile.com/oauth/token'

def oauth2_url(auth_uri, client_id, redirect_uri):
    return '%(auth_uri)s?redirect_uri=%(redirect_uri)s&response_type=token&client_id=%(client_id)s' % {'auth_uri': auth_uri,
                                                                                                      'client_id': quote(client_id),
                                                                                                      'redirect_uri': quote(redirect_uri)}


def oauth2_token(token_uri, client_id, client_secret, code, redirect_uri):
    payload = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        }
    return json.loads(requests.post(token_uri, data=payload).content)
    

def register_geoloqi(request):
    auth_url = oauth2_url(GEOLOQI_AUTH_URI, settings.GEOLOQI_CLIENT_ID, settings.GEOLOQI_REDIRECT_URI)
    return HttpResponseRedirect(auth_url)


@render_to('core/success.html')
def register_geoloqi_callback(request):
    auth_stuff = oauth2_token(GEOLOQI_TOKEN_URI,
                              settings.GEOLOQI_CLIENT_ID,
                              settings.GEOLOQI_CLIENT_SECRET,
                              request.GET['code'],
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

    return locals()

@login_required
def register_dailymile(request):
    auth_url = oauth2_url(DAILYMILE_AUTH_URI, settings.DAILYMILE_CLIENT_ID, settings.DAILYMILE_REDIRECT_URI)
    return HttpResponseRedirect(auth_url)


@login_required
@render_to('core/success.html')
def register_dailymile_callback(request):
    auth_stuff = oauth2_token(DAILYMILE_TOKEN_URI,
                              settings.DAILYMILE_CLIENT_ID,
                              settings.DAILYMILE_CLIENT_SECRET,
                              request.GET['code'],
                              settings.DAILYMILE_REDIRECT_URI)

    DailyMileProfile.objects.create(user=request.user,
                                    access_token=auth_stuff['access_token'])
    return locals()
