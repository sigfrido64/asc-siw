# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Home page dell'applicazione.
@login_required()
def si_home(request):
    return render(request, 'home.html')
