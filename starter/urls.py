from django.conf.urls import url
from django.urls import path

from .views import *


app_name = 'starter'

urlpatterns = [
    path('', index, name='index'),
    path('start', start, name='start'),
    path('up', up, name='up'),
]
