from django.conf.urls import url
from django.urls import path

from .views import *


app_name = 'starter'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('up', up, name='up'),
    path('ip', ip, name='ip'),
]
