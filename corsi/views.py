# coding=utf-8
from django.shortcuts import render, get_object_or_404, redirect
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models import Corso
from .forms import CorsoForm


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
        form = CorsoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('corsi:home')
        else:
            print(form.errors)
    else:
        form = CorsoForm()
    return render(request, 'corsi/inserisce_modifica_corso.html', {'corso': form})


@has_permission_decorator(SiwPermessi.CORSI_MODIFICA)
def corso_modifica_view(request, pk):
    corso = get_object_or_404(Corso, pk=pk)
    if request.method == 'POST':
        form = CorsoForm(request.POST, instance=corso)
        if form.is_valid():
            form.save()
            return redirect('corsi:home')
    else:
        cdc_txt = corso.cdc.nome
        form = CorsoForm(instance=corso, initial={'cdc_txt': cdc_txt})
    return render(request, 'corsi/inserisce_modifica_corso.html', {'corso': form})
