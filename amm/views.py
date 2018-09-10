# coding=utf-8
from django.shortcuts import render
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models.centri_di_costo import CentroDiCosto


@has_permission_decorator(SiwPermessi.AMM_CDC_READ)
def cdc(request):
    # Compongo la lista degli anni formativi
    iniziative = CentroDiCosto.objects.all()
    return render(request, 'amm/cdc.html', {'iniziative': iniziative})
