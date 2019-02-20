from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
import time, datetime
from .models import LogTime
import datetime

sys_state = "down"
update_time = time.time()
heartbeat_time = 0


def update_sys_state(state):
    global sys_state, update_time
    if sys_state != state:
        log = LogTime.objects.create(
            fr=datetime.datetime.fromtimestamp(update_time),
            to=datetime.datetime.fromtimestamp(time.time()),
            tot_seconds=time.time() - update_time,
            state=sys_state
        )
        log.save()
        sys_state = state
        update_time = time.time()


def index(request):
    global sys_state, update_time, heartbeat_time

    # Update sys state
    if time.time() - heartbeat_time > 90:
        update_sys_state("down")

    state = sys_state
    last_update_passed = 1000 * (time.time() - update_time)
    return render(request, 'index.html', locals())


def up(request):
    global sys_state, update_time, heartbeat_time
    heartbeat_time = time.time()
    update_sys_state("up")
    return HttpResponse("OK")


def start(request):
    if not request.user.is_authenticated:
        raise Http404
    global sys_state, update_time, heartbeat_time
    if sys_state == "down":
        update_sys_state("starting")
        heartbeat_time = time.time()
    return redirect('starter:index')
