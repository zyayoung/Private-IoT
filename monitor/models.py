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
    delta = models.BooleanField(blank=True, default=False)
    priority = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

    def data(self):
        return Data.objects.filter(slot=self)

    def latest_value(self):
        if self.data().exists():
            obj = self.data().order_by('-time')[0]
            if obj.time.timestamp() + 3600 > time.time():
                if self.delta:
                    try:
                        last_obj = self.data().order_by('-time')[1]
                        return round((obj.value - last_obj.value) * self.scale_factor / (obj.time.timestamp() - last_obj.time.timestamp()), 3)
                    except IndexError:
                        return '--'
                else:
                    return round(obj.value * self.scale_factor, 3)
            else:
                return '--'
        else:
            return '--'

    def process(self, data):
        jump = max(1, data.count()//1000)
        if self.delta:
            last = None
            last_time = 0
            ret = []
            for d in data.values_list('time', 'value')[::jump]:
                if last is not None and d[1] >= last:
                    ret.append([d[0].timestamp(), (d[1] - last) / (d[0].timestamp()-last_time)])
                last = d[1]
                last_time = d[0].timestamp()
            return ret
        else:
            return [[values[0].timestamp(), values[1]] for values in data.values_list('time', 'value')[::jump]]

    def full_data(self):
        return self.process(self.data())

    def less_data(self, seconds=3600):
        return self.process(self.data().filter(
            time__gt=datetime.datetime.fromtimestamp(time.time()-seconds)
        ))

    def max_time(self):
        return '%.3f' % time.time()

    class Meta:
        ordering = ['-priority']


class Data(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
