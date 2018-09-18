# coding=utf-8
from django.http import JsonResponse
from django.db.models import F

from .models.centri_di_costo import CentroDiCosto


# @ajax_has_permission_decorator(SiwPermessi.COLLABORATORE_INSERISCE)
def ajax_centri_di_costo_per_treeview(request):
    cdc = CentroDiCosto.objects.all()
    cdc = cdc.values('id', 'parent', 'nome')
    cdc_list = list(cdc)
    print('debug')
    print(cdc_list)
    return JsonResponse(cdc_list, safe=False)
