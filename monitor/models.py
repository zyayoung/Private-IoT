from django.db import models


class Slot(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def values(self):
        return Data.objects.filter(slot=self)


class Data(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
