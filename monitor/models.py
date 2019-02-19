from django.db import models
import time

class Slot(models.Model):
    name = models.CharField(max_length=64)

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
