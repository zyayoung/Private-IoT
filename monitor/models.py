from django.db import models
import time
import datetime


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

    def latest_value(self):
        if self.data().exists():
            obj = self.data().order_by('-time')[0]
            if obj.time.timestamp() + 3600 > time.time():
                return "%.2f" % (obj.value * self.scale_factor, )
            else:
                return '--'
        else:
            return '--'

    def full_data(self):
        return [[values[0].timestamp(), values[1]] for values in self.data().values_list('time', 'value')]

    def less_data(self):
        return [[values[0].timestamp(), values[1]] for values in self.data().filter(
            time__gt=datetime.datetime.fromtimestamp(time.time()-3600)
        ).values_list('time', 'value')]

    def max_time(self):
        return '%.3f' % time.time()


class Data(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
