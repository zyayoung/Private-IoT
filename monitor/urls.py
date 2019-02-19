from django.conf.urls import url

from .views import *


app_name = 'monitor'

urlpatterns = [
    url(r'^$', ListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(), name='detail'),
    url(r'^add$', add_data, name='add'),
]