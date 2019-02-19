from django.db import models


class LogTime(models.Model):
    fr = models.DateTimeField()
    to = models.DateTimeField()
    tot_seconds = models.FloatField()
    state = models.CharField(max_length=32)
