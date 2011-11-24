from django.db import models
from core import WORKOUT_TYPE_CHOICES

class OAuth2BaseModel(models.Model):
    oauth_user_id = models.CharField(max_length=20, blank=True, null=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class GeoloqiProfile(OAuth2BaseModel):
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return self.user.username


class DailyMileProfile(OAuth2BaseModel):
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return self.user.username


class Workout(models.Model):
    user = models.ForeignKey('core.GeoloqiProfile')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
    workout_type = models.PositiveIntegerField(choices=WORKOUT_TYPE_CHOICES)
