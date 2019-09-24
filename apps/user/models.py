from django.db import models


class Settings(models.Model):
    volume = models.CharField(max_length=5, default="mt")
