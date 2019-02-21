from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
import time
from .models import LogTime, AutoShutdownThreshold
import datetime
import threading as td
import os

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


def check_up(wait=0):
    if wait:
        time.sleep(wait)
    # Update sys state
    global heartbeat_time
    if time.time() - heartbeat_time > 150:
        update_sys_state("down")


def check_daemon():
    while True:
        check_up(60)
        if sys_state == "up" and time.time() - update_time > 600 and AutoShutdownThreshold.objects.exists():
            # Auto Shutdown
            shutdown_now = []
            for threshold in AutoShutdownThreshold.objects.all():
                shutdown_now.append(threshold.shutdown())
            if shutdown_now and False not in shutdown_now:
                update_sys_state("shutting down")
                print("Auto shutdown")


check_t = td.Thread(target=check_daemon, daemon=True)
check_t.start()


class Index(generic.View):
    def get(self, request):
        global sys_state, update_time, heartbeat_time

        # Update sys state
        check_up()

        state = sys_state
        last_update_passed = 1000 * (time.time() - update_time)
        return render(request, 'index.html', locals())

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Not authenticated')
        global sys_state, update_time, heartbeat_time
        if sys_state == "down" or sys_state == "up":
            if sys_state == "down":
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
                GPIO.output(18, GPIO.HIGH)
                time.sleep(0.8)
                GPIO.output(18, GPIO.LOW)
            update_sys_state("starting" if sys_state == "down" else "shutting down")
            heartbeat_time = time.time()
        return redirect('starter:index')


def up(request):
    global sys_state, update_time, heartbeat_time
    if sys_state != "shutting down":
        heartbeat_time = time.time()
        update_sys_state("up")
        return HttpResponse("OK")
    else:
        return HttpResponse("Shutting down")


def ip(request):
    return HttpResponse(os.popen("hostname -I").read())
