# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from .models import Spesa
from siw.sig_utils import from_choices_to_list


def ajax_lista_stati_spesa(request):
    tipo_spese = Spesa.STATO_SPESA_CHOICES
    return from_choices_to_list(tipo_spese)


def ajax_lista_tipo_spesa_2(request):
    lista = list()
    for tipo in Spesa.TIPO_SPESA_CHOICES:
        if 100 < tipo[0] < 300:
            lista.append(tipo)
    return from_choices_to_list(lista)


def ajax_lista_tipo_spesa_1(request):
    lista = list()
    for tipo in Spesa.TIPO_SPESA_CHOICES:
        if tipo[0] < 100:
            lista.append(tipo)
    return from_choices_to_list(lista)
