# coding=utf-8
import time
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Persona
from siw.sqlserverinterface import sqlserverinterface
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models import Collaboratore


# Create your views here.
@has_permission_decorator(SiwPermessi.COLLABORATORI_LISTA_READ)
def lista_collaboratori_view(request):
    # Devo prendere la lista con cognome, nome e poi mettere un link per i dettagli.
    collaboratori = Collaboratore.objects.all()
    return render(request, 'collaboratori/lista_collaboratori.html', {'collaboratori': collaboratori})


@has_permission_decorator(SiwPermessi.COLLABORATORE_MOSTRA)
def mostra_collaboratore_view(request, pk):
    collaboratore = get_object_or_404(Collaboratore, pk=pk)
    return render(request, 'collaboratori/mostra_collaboratore.html', {'collaboratore': collaboratore})


@has_permission_decorator(SiwPermessi.COLLABORATORE_INSERISCE)
def propone_inserimento_collaboratore_view(request):
    return render(request, 'collaboratori/inserisce_collaboratore.html')


@has_permission_decorator(SiwPermessi.COLLABORATORE_INSERISCE)
def inserisce_nuovo_collaboratore_view(request, pk_persona):
    return HttpResponse("Ciao")
