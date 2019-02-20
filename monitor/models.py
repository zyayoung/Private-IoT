from django.db import models
import time


class Slot(models.Model):
    name = models.CharField(max_length=64)
    auto_range = models.BooleanField(blank=True, default=True)
    min = models.FloatField(blank=True, default=0)
    max = models.FloatField(blank=True, default=0)
    scale_factor = models.FloatField(blank=True, default=1)
    unit = models.CharField(max_length=64, blank=True, default='')

    def __str__(self):
        return self.name

    def data(self):
        return Data.objects.filter(slot=self)

    def full_data(self):
        data = []
        for value in self.data():
            data.append(['%.3f' % value.time.timestamp(), value.value])
        return data

    def max_time(self):
        return '%.3f' % time.time()


class Data(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
