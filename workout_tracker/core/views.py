from urllib import quote
from django.conf import settings
from django.http import HttpResponseRedirect
import requests


AUTH_URI = 'https://geoloqi.com/oauth/authorize'
TOKEN_URI = 'https://api.geoloqi.com/1/oauth/token'

def register(request):
    auth_url = '%(auth_uri)s?redirect_uri=%(redirect_uri)s&response_type=code&client_id=%(client_id)s' % {'auth_uri': AUTH_URI,
                                                                                                          'client_id': quote(settings.GEOLOQI_CLIENT_ID),
                                                                                                          'redirect_uri': quote(settings.REDIRECT_URI)}
    return HttpResponseRedirect(auth_url)


def login(request):
    payload = {
        'grant_type': 'authorization_code',
        'client_id': settings.GEOLOQI_CLIENT_ID,
        'client_secret': settings.GEOLOQI_CLIENT_SECRET,
        'code': request.GET['code'],
        'redirect_uri': settings.REDIRECT_URI,
        }
    response = requests.post(TOKEN_URI, data=payload)
