# coding=utf-8
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from collaboratori.models import Collaboratore
from anagrafe.models import Persona, TipoTelefonoPersone, TipoMailPersone
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


@ajax_has_permission_decorator(SiwPermessi.COLLABORATORE_INSERISCE)
def ajax_check_persona_for_possible_collaborator(request):
    pk_persona = request.GET.get('pk_persona', 0)

    try:
        collaboratore = Collaboratore.objects.get(persona__pk=pk_persona)
    except ObjectDoesNotExist:
        persona = Persona.objects.get(pk=pk_persona)
        risposta = render_to_string("collaboratori/includes/informa_collaboratore_inseribile.html",
                                    {'persona': persona})
        return JsonResponse({'html': risposta}, safe=False)
    risposta = render_to_string("collaboratori/includes/errore_collaboratore_gia_presente.html",
                                {'collaboratore': collaboratore})
    return JsonResponse({'html': risposta}, safe=False)


def ajax_tipi_telefono_persone(request):
    tipo_telefono = TipoTelefonoPersone.objects.all()
    tipo_telefono = tipo_telefono.values('descrizione_telefono', 'pk')
    # Per convertire in Json devo prima convertire in lista.
    tipo_telefono_list = list(tipo_telefono)
    return JsonResponse(tipo_telefono_list, safe=False)


def ajax_tipi_mail_persone(request):
    tipo_mail = TipoMailPersone.objects.all()
    tipo_mail = tipo_mail.values('descrizione_mail', 'pk')
    # Per convertire in Json devo prima convertire in lista.
    tipo_mail_list = list(tipo_mail)
    return JsonResponse(tipo_mail_list, safe=False)
