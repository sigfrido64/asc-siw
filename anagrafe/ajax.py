# coding=utf-8
from django.shortcuts import render, get_object_or_404
from anagrafe.models import Persona
from siw.decorators import ajax_has_permission_decorator
from accounts.models import SiwPermessi


@ajax_has_permission_decorator(SiwPermessi.ANAGRAFE_DETTAGLIO_PERSONA_MOSTRA)
def ajax_dettaglio_persona_view(request, pk_persona):
    persona = get_object_or_404(Persona, pk=pk_persona)
    return render(request, 'anagrafe/dettaglio_persona.html', {'persona': persona})
