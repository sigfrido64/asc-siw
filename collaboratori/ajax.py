# coding=utf-8
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import Collaboratore
from anagrafe.models import Persona
from siw.decorators import ajax_has_permission_decorator
from accounts.models import SiwPermessi


@ajax_has_permission_decorator(SiwPermessi.COLLABORATORE_INSERISCE)
def ajax_load_tutte_persone(request):
    name_starts_with = request.GET.get('name_starts_with', '')
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


def ajax_check_persona_for_possible_collaborator(request):
    pk_persona = request.GET.get('pk_persona', 0)

    if collaboratore_gia_presente(pk_persona):
        return render(request, 'collaboratori/includes/corsi_list_options.html', {'corsi': lista_corsi(anno)})

    return HttpResponse("Testa di quiz! ")
    """
    if collaboratore_gia_presente(pk_persona):
        
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
    """


def collaboratore_gia_presente(pk_persona):
    return False
    # collaboratore = Collaboratore.objects.get(persona=pk_persona)
    