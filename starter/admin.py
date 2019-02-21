from django.contrib import admin
from .models import LogTime, AutoShutdownThreshold


class LogTimeAdmin(admin.ModelAdmin):
    list_display = ('fr', 'to', 'tot_seconds', 'state')
    list_filter = ('state', )
    date_hierarchy = 'to'


class AutoShutdownThresholdAdmin(admin.ModelAdmin):
    list_display = ('slot', 'value', 'hold_seconds', 'shutdown')


admin.site.register(LogTime, LogTimeAdmin)
admin.site.register(AutoShutdownThreshold, AutoShutdownThresholdAdmin)
