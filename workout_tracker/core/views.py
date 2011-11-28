import json
from urllib import quote

from annoying.decorators import render_to
import requests
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from core import GEOLOQI_AUTH_URI, GEOLOQI_TOKEN_URI, DAILYMILE_AUTH_URI, DAILYMILE_TOKEN_URI, oauth2_url
from core.models import GeoloqiProfile, DailyMileProfile



def register_geoloqi(request):
    auth_url = oauth2_url(GEOLOQI_AUTH_URI, settings.GEOLOQI_CLIENT_ID, settings.GEOLOQI_REDIRECT_URI)
    return HttpResponseRedirect(auth_url)


@render_to('core/success.html')
def register_geoloqi_callback(request):
    user = authenticate(code=request.GET['code'])
    if user:
        login(request, user)
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


@login_required
@render_to('workout/start.html')
def workout_start(request, workout_type_id):
    force_ended_workouts = Workout.force_end_workouts_in_progress(request.user)
    Workout.object.create(user=request.user, workout_type=workout_type_id)
