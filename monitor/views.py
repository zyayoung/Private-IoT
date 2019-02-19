from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import *
from django.http import HttpResponse, Http404
import time


class ListView(generic.ListView):
    template_name = 'monitor/list.html'
    context_object_name = 'slots'

    def get_queryset(self):
        return Slot.objects.all()


class DetailView(generic.DetailView):
    template_name = 'monitor/detail.html'
    model = Slot
    server_time = '%.3f' % time.time()


def add_data(request):
    value = request.GET.get('value', '0')
    slot = request.GET.get('slot', None)
    if slot:
        data = Data.objects.create(
            slot=get_object_or_404(Slot, id=slot),
            value=value,
        )
        data.save()
        return HttpResponse('OK')
    else:
        raise Http404
