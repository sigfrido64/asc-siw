# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models import Iniziativa, Progetto, SottoProgetto


@has_permission_decorator(SiwPermessi.AMM_CDC_READ)
def cdc(request):
    # Compongo la lista degli anni formativi
    iniziative = Iniziativa.objects.all()
    progetti = Progetto.objects.all()
    sottoprogetti = SottoProgetto.objects.all()
    return render(request, 'amm/cdc.html', {'iniziative': iniziative, 'progetti': progetti, 'sottoprogetti':
        sottoprogetti})
