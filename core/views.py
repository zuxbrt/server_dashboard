from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.http import JsonResponse

import random, json
import sys
import os
import psutil
from psutil._common import bytes2human

from django.contrib.auth import authenticate, login as adminlogin, logout as adminlogout

# index page
def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render(request, 'login.html')

# dashboard
def dashboard(request):
    if request.user.is_authenticated:
        context = {}
        context["cpu_usage"] = json.dumps(psutil.cpu_percent(interval=None, percpu=False))

        total_memory = psutil.virtual_memory()

        dict(psutil.virtual_memory()._asdict())
        # you can have the percentage of used RAM
        used_ram = psutil.virtual_memory().percent
        available_ram = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

        context["free_ram"] = json.dumps(available_ram)
        context["used_ram"] = json.dumps(used_ram)

        disk_usage = []
        for part in psutil.disk_partitions(all=False):
                if os.name == 'nt':
                    if 'cdrom' in part.opts or part.fstype == '':
                        # skip cd-rom drives with no disk in it; they may raise
                        # ENOENT, pop-up a Windows GUI error for a non-ready
                        # partition or just hang.
                        continue
                usage = psutil.disk_usage(part.mountpoint)
                disk_usage.append(
                    {
                        "device": part.device,
                        "total": bytes2human(usage.total),
                        "used": bytes2human(usage.used),
                        "free": bytes2human(usage.free),
                        "percent": int(usage.percent),
                        "fs_type": part.fstype,
                        "mountpoint": part.mountpoint
                    })
        context["disk_usage"] = json.dumps(disk_usage)
        
        return render(request, 'index.html', context)
    else:
        return render(request, 'login.html')

# get stats
def get_stats(request):
    context = {}
    context["cpu_usage"] = json.dumps(psutil.cpu_percent(interval=None, percpu=False))

    total_memory = psutil.virtual_memory()

    dict(psutil.virtual_memory()._asdict())
    used_ram = psutil.virtual_memory().percent
    available_ram = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

    context["free_ram"] = json.dumps(available_ram)
    context["used_ram"] = json.dumps(used_ram)

    disk_usage = []
    for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    # skip cd-rom drives with no disk in it; they may raise
                    # ENOENT, pop-up a Windows GUI error for a non-ready
                    # partition or just hang.
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            disk_usage.append(
                {
                    "device": part.device,
                    "total": bytes2human(usage.total),
                    "used": bytes2human(usage.used),
                    "free": bytes2human(usage.free),
                    "percent": int(usage.percent),
                    "fs_type": part.fstype,
                    "mountpoint": part.mountpoint
                })
    context["disk_usage"] = json.dumps(disk_usage)

    return JsonResponse(context)

# login user
def admin_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        adminlogin(request, user)
        return redirect('/dashboard')
    else:
        return render(request, 'login.html', {
            'error_message': "Bad credentials"
        })

# logout user
def admin_logout(request):
    adminlogout(request)
    return HttpResponseRedirect('/')

