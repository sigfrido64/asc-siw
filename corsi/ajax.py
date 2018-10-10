# coding=utf-8
from django.http import JsonResponse
from .models import Corso


def ajax_lista_stati_corso(request):
    stati_corso = Corso.STATO_CORSO_CHOICES
    stati_corso_list = list()
    for stato_corso in stati_corso:
        stato = dict()
        stato['id'] = stato_corso[0]
        stato['descrizione'] = stato_corso[1]
        stati_corso_list.append(stato)
    # Per convertire in Json devo prima convertire in lista.
    # stati_corso_list = list(stati_corso)
    return JsonResponse(stati_corso_list, safe=False)
