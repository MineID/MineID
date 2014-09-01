from django.db import models
from django.contrib.auth import get_user_model

from .avatar import get_minecraft_avatar
from .managers import MinecraftAccountManager


class MinecraftAccount(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name='minecraft_accounts')
    profile = models.CharField(max_length=75)
    profile_id = models.CharField(max_length=32, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    primary = models.BooleanField(default=False)

    objects = MinecraftAccountManager()

    class Meta:
        unique_together = ('user', 'primary')

    def get_avatar(self, geometry_string):
        return get_minecraft_avatar(self.profile, geometry_string)

    def get_api_dict(self, base_url):
        return {
            'name': self.profile,
            'uid': self.profile_id,
            'avatar': base_url + self.get_avatar('64x64'),
        }
