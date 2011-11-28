import json
from urllib import quote

import requests


WORKOUT_TYPE_RUNNING = 1
WORKOUT_TYPE_CYCLING = 2
WORKOUT_TYPE_HIKING = 3

WORKOUT_TYPE_CHOICES = (
    (WORKOUT_TYPE_RUNNING, 'Running'),
    (WORKOUT_TYPE_CYCLING, 'Cycling'),
    (WORKOUT_TYPE_HIKING, 'Hiking'),
)

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
