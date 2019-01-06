# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.http import JsonResponse
from .models import AcquistoConOrdine
from siw.sig_utils import from_choices_to_list
from siw.decorators import ajax_has_permission_decorator
from accounts.models import SiwPermessi
from anagrafe.models import Fornitore


def ajax_lista_stati_ordine(request):
    return from_choices_to_list(AcquistoConOrdine.STATO_ORDINE_CHOICES)


def ajax_lista_tipo_spesa_2(request):
    lista = list()
    for tipo in AcquistoConOrdine.STATO_ORDINE_CHOICES:
        if 100 < tipo[0] < 300:
            lista.append(tipo)
    return from_choices_to_list(lista)


def ajax_lista_tipo_ordini(request):
    return from_choices_to_list(AcquistoConOrdine.TIPO_ORDINE_CHOICES)


def ajax_lista_fornitori(request):
    fornitori = Fornitore.objects.filter(in_uso=True)
    fornitori = fornitori.values('azienda__ragione_sociale', 'pk')
    # Per convertire in Json devo prima convertire in lista.
    fornitori_list = list(fornitori)
    return JsonResponse(fornitori_list, safe=False)


@ajax_has_permission_decorator(SiwPermessi.ACQUISTI_CDC_ERASE)
def ajax_elimina_ripartizione_su_cdc(request):
    pass