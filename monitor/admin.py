from django.contrib import admin
from .models import *


class DataAdmin(admin.ModelAdmin):
    list_display = ('time', 'slot', 'value')
    list_filter = ('slot', )
    date_hierarchy = 'time'


admin.site.register(Slot)
admin.site.register(Data, DataAdmin)
