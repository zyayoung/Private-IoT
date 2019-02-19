from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
import time, datetime
from .models import LogTime

sys_state = "down"
update_time = time.clock()
heartbeat_time = 0


def update_sys_state(state):
    global sys_state, update_time
    if sys_state != state:
        sys_state = state
        log = LogTime.objects.create(
            fr=time.localtime(update_time),
            to=time.localtime(time.clock()),
            tot_seconds=time.clock() - update_time
        )
        log.save()
        update_time = time.clock()


def index(request):
    global sys_state, update_time, heartbeat_time

    # Update sys state
    if time.clock() - heartbeat_time > 90:
        update_sys_state("down")

    state = sys_state
    last_update_passed = 1000 * (time.clock() - update_time)
    return render(request, 'index.html', locals())


def up(request):
    global sys_state, update_time, heartbeat_time
    heartbeat_time = time.clock()
    update_sys_state("up")
    return HttpResponse("OK")


def start(request):
    if not request.user.is_authenticated:
        raise Http404
    global sys_state, update_time, heartbeat_time
    if sys_state == "down":
        update_sys_state("starting")
    return redirect('starter:index')
