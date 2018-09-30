# coding=utf-8
from django.shortcuts import render
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models import Corso


@has_permission_decorator(SiwPermessi.CORSI_LISTA_READ)
def corsi_list_home(request):
    lista_corsi = Corso.objects.all()
    return render(request, 'corsi/lista_corsi.html', {'lista_corsi': lista_corsi})

