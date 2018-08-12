# coding=utf-8
from django.http import JsonResponse
from .models import Persona


def ajax_load_tutte_persone(request):
    name_starts_with = request.GET.get('name_starts_with')
    if len(name_starts_with) > 2:
        limite = 200
    else:
        limite = 100
    persone = Persona.objects.all()
    persone = persone.values('cognome', 'nome', 'data_nascita', 'pk')
    persone = persone.filter(cognome__startswith=name_starts_with)
    persone = persone.order_by('cognome', 'nome')[:limite]
    # Per convertire in Json devo prima convertire in lista.
    persone_list = list(persone)
    return JsonResponse(persone_list, safe=False)
