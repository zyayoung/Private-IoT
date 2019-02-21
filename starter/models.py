from django.db import models
from monitor.models import Slot


class LogTime(models.Model):
    fr = models.DateTimeField()
    to = models.DateTimeField()
    tot_seconds = models.FloatField()
    state = models.CharField(max_length=32)


class AutoShutdownThreshold(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    value = models.FloatField()
    hold_seconds = models.IntegerField(default=1800)

    def __str__(self):
        return self.slot.name

    def shutdown(self):
        data = self.slot.less_data(self.hold_seconds)
        if len(data) < self.hold_seconds * 0.8 / 60:
            return False
        shutdown_now = True
        for t, v in data:
            if v >= self.value:
                shutdown_now = False
                break
        return shutdown_now
