# -*- coding: utf-8 -*-

import json
import urllib
import urllib.request
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Log
from foledol.django.utils import get_param, check_length, send_mail2


def user_login(request):
    error = None
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(settings.DEFAULT_SPACE + ':home'))
        if len(User.objects.filter(username=username)) < 1:
            error = "Ce nom d'utilisateur est inconnu"
        else:
            error = "Le mot de passe est incorrect"
    context = {'error': error}
    return render(request, 'user_login.html', context)


def user_logout(request):
    logout(request)
    return render(request, 'user_logout.html')

