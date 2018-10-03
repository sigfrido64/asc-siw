# coding=utf-8
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models import Corso
from amm.models.centri_di_costo import CentroDiCosto
from .forms import NewCorsoForm


@has_permission_decorator(SiwPermessi.CORSI_LISTA_READ)
def corsi_list_home(request):
    lista_corsi = Corso.objects.all()
    return render(request, 'corsi/lista_corsi.html', {'lista_corsi': lista_corsi})


@has_permission_decorator(SiwPermessi.CORSI_MOSTRA)
def corso_dettaglio_view(request, pk):
    corso = get_object_or_404(Corso, pk=pk)
    return render(request, 'corsi/dettaglio_corso.html', {'corso': corso})


@has_permission_decorator(SiwPermessi.CORSI_INSERISCE)
def corso_inserisce_view(request):
    if request.method == 'POST':
        form = NewCorsoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('corsi:home')
    else:
        form = NewCorsoForm()
    return render(request, 'corsi/inserisce_corso.html', {'corso': form})


# @has_permission_decorator(SiwPermessi.CORSI_MODIFICA)
def corso_modifica_view(request, pk):
    corso = get_object_or_404(Corso, pk=pk)
    if request.method == 'POST':
        form = NewCorsoForm(request.POST, instance=corso)
        if form.is_valid():
            form.save()
            return redirect('corsi:home')
    else:
        form = NewCorsoForm(instance=corso)
    return render(request, 'corsi/inserisce_corso.html', {'corso': form})
