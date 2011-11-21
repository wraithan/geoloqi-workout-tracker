from django.db import models


class OAuth2BaseModel(models.Model):
    oauth_user_id = models.CharField(max_length=20)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    class Meta:
        abstract = True


class GeoLoqiProfile(OAuth2BaseModel):
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return self.user.username
