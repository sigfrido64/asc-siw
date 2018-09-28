# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from siw.decorators import ajax_has_permission_decorator
from accounts.models import SiwPermessi
from .models.centri_di_costo import CentroDiCosto


@ajax_has_permission_decorator(SiwPermessi.AMM_CDC_READ)
def ajax_centri_di_costo_per_treeview(request):
    cdc = CentroDiCosto.objects.all()
    cdc = cdc.values('id', 'parent', 'nome')
    cdc_list = list(cdc)
    return JsonResponse(cdc_list, safe=False)


@ajax_has_permission_decorator(SiwPermessi.AMM_CDC_READ)
def ajax_centro_di_costo_dettaglio(request):
    # Recupero i parametri di GET
    cdc_id = request.GET.get('cdcId')
    
    cdc = CentroDiCosto.objects.get(id=cdc_id)
    return render(request, 'amm/cdc_detail.html', {'cdc': cdc})
