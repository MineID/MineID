from django.db import models


class MinecraftAccountManager(models.Manager):
    def primary(self):
        return self.filter(primary=True).first()
