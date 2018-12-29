# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from siw.decorators import ajax_has_permission_decorator
from accounts.models import SiwPermessi
from .models.centri_di_costo import CentroDiCosto
from .models.mixins import AnnoFormativo


@ajax_has_permission_decorator((SiwPermessi.AMM_CDC_READ, SiwPermessi.CORSI_INSERISCE, SiwPermessi.CORSI_MODIFICA))
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


def ajax_load_af(request):
    anno_formativo = AnnoFormativo.objects.all()
    anno_formativo = anno_formativo.values('anno_formativo', 'pk')
    # Per convertire in Json devo prima convertire in lista.
    anno_formativo_list = list(anno_formativo)
    return JsonResponse(anno_formativo_list, safe=False)


def ajax_set_af(request):
    # Recupera il parametro di anno_formativo
    anno_formativo = request.GET.get('anno_formativo', '')
    
    # Se coincide con un valore del data base ne prende la pk, altrimenti prende i valori da quello di default
    try:
        anno_formativo_obj = AnnoFormativo.objects.get(anno_formativo=anno_formativo)
        anno_formativo_pk = anno_formativo_obj.pk
    except ObjectDoesNotExist:
        anno_formativo_obj = AnnoFormativo.objects.get(default=True)
        anno_formativo = anno_formativo_obj.anno_formativo
        anno_formativo_pk = anno_formativo_obj.pk
        
    # Setta i dati nella sessione.
    request.session['anno_formativo'] = anno_formativo
    request.session['anno_formativo_pk'] = anno_formativo_pk
    return JsonResponse({'risultato': 'ok'}, safe=False)
