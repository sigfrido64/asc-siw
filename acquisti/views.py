# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.shortcuts import render, HttpResponse, redirect
from accounts.models import SiwPermessi
from siw.decorators import has_permission_decorator
from .models import Spesa
from .forms import NewSpesaTipo2Form


# Create your views here.
def spese_home(request):
    spese = Spesa.objects.filter(anno_formativo=request.session['anno_formativo_pk'])
    return render(request, 'spese/lista_spese.html', {'spese': spese})


def aggiorna_spese(request):
    spese = Spesa.objects.filter(anno_formativo=request.session['anno_formativo_pk'], dirty=True)
    for spesa in spese:
        spesa.calcola_costo_totale()
    return HttpResponse("Fatto !")


@has_permission_decorator(SiwPermessi.SPESE_INSERISCE_NUOVA)
def inserisce_spesa(request):
    if request.method == 'POST':
        form = NewSpesaTipo2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('acquisti:home')
        else:
            print(form.errors)
    else:
        form = NewSpesaTipo2Form()
    return render(request, 'spese/inserisce_spesa.html', {'spesa': form})
