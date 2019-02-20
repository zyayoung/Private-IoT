from django.contrib import admin
from .models import LogTime


class LogTimeAdmin(admin.ModelAdmin):
    list_display = ('fr', 'to', 'tot_seconds', 'state')
    list_filter = ('state', )
    date_hierarchy = 'to'


admin.site.register(LogTime, LogTimeAdmin)
