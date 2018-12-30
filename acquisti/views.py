# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.shortcuts import render, HttpResponse
from .models import Spesa


# Create your views here.
def spese_home(request):
    spese = Spesa.objects.filter(anno_formativo=request.session['anno_formativo_pk'])
    return render(request, 'spese/lista_spese.html', {'spese': spese})


def aggiorna_spese(request):
    spese = Spesa.objects.filter(anno_formativo=request.session['anno_formativo_pk'], dirty=True)
    for spesa in spese:
        spesa.calcola_costo_totale()
    return HttpResponse("Fatto !")

