# coding=utf-8
import time
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Persona
from siw.sqlserverinterface import sqlserverinterface
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models import Collaboratore
from siw.sig_debug import response_debug
from siw.decorators import ajax_has_permission_decorator
from django.db.models import Value
from django.db.models.functions import Concat, Str


def ajax_load_tutte_persone(request):
    print("Chiamata Ajax")
    starts_with = request.GET.get('name_starts_with')

    if len(starts_with) > 2:
        limite = 200
    else:
        limite = 100
    # queryset = Item.objects.annotate(search_name=Concat('series', Value(' '), 'number'))
    # then you can filter:
    # queryset.filter(search_name__icontains='whatever text')

    persone = Persona.objects.all().annotate(persona=Concat('cognome', Value(' '), 'nome', Value(' '), 'pk'))
    persone = persone.values('persona', 'pk')
    persone = persone.filter(persona__startswith=starts_with)
    persone = persone.order_by('persona')[:limite]
    print('Query : ', persone.query)

    # Per tradurre in Json devo convertire in lista.
    persone_list = list(persone)
    return JsonResponse(persone_list, safe=False)
