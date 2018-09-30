# coding=utf-8
from django.shortcuts import render, get_object_or_404
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models import Corso


@has_permission_decorator(SiwPermessi.CORSI_LISTA_READ)
def corsi_list_home(request):
    lista_corsi = Corso.objects.all()
    return render(request, 'corsi/lista_corsi.html', {'lista_corsi': lista_corsi})


@has_permission_decorator(SiwPermessi.CORSI_MOSTRA)
def corso_dettaglio_view(request, pk):
    corso = get_object_or_404(Corso, pk=pk)
    return render(request, 'corsi/dettaglio_corso.html', {'corso': corso})


def corso_inserisce_view(request, pk):
    pass
    """
    corso = get_object_or_404(Corso, pk=pk)
    return render(request, 'corsi/dettaglio_corso.html', {'corso': corso})
    """