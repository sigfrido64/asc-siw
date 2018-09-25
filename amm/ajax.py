# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from .models.centri_di_costo import CentroDiCosto


# @ajax_has_permission_decorator(SiwPermessi.COLLABORATORE_INSERISCE)
def ajax_centri_di_costo_per_treeview(request):
    cdc = CentroDiCosto.objects.all()
    cdc = cdc.values('id', 'parent', 'nome')
    cdc_list = list(cdc)
    print('debug')
    print(cdc_list)
    return JsonResponse(cdc_list, safe=False)


def ajax_centro_di_costo_dettaglio(request):
    # Recupero i parametri di GET
    cdc_id = request.GET.get('cdcId')
    
    cdc = CentroDiCosto.objects.get(id=cdc_id)
    return render(request, 'amm/cdc_detail.html', {'cdc': cdc})
