from datetime import datetime

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

    def get_current_workout(self):
        workouts = self.workout_set.filter(end=None)
        if workouts.exists():
            return workouts.get()
        else:
            return None


class DailyMileProfile(OAuth2BaseModel):
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return self.user.username


class Workout(models.Model):
    geoloqi_profile = models.ForeignKey('core.GeoloqiProfile')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
    shipped = models.BooleanField(default=False)
    workout_type = models.ForeignKey('core.WorkoutType', null=True)

    def __unicode__(self):
        return u"from %s to %s" % (self.start, self.end)

    def save(self, forced_end=False, *args, **kwargs):
        super(Workout, self).save(*args, **kwargs)

        if not forced_end and not self.shipped and self.end is not None:
            self.ship_to_trackers()

    def ship_to_trackers(self):
        pass

    @classmethod
    def force_end_workouts_in_progress(cls, geoloqi_profile):
        unfinished_workouts = geoloqi_profile.workout_set.filter(end=None)

        if unfinished_workouts.exists():
            for uw in unfinished_workouts:
                uw.end = datetime.now()
                uw.save(forced_end=True)
            return True
        return False

    def finish_workout(self):
        if not self.end:
            self.end = datetime.now()
            self.save()
            return True
        return False


class WorkoutType(models.Model):
    name = models.CharField(max_length=255)
