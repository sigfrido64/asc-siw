# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.shortcuts import render, HttpResponse, redirect
from accounts.models import SiwPermessi
from siw.decorators import has_permission_decorator
from siw.sig_utils import get_anno_formativo
from .models import Spesa
from .forms import NewSpesaTipo2Form, NewSpesaTipo1Form


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
def inserisce_altra_spesa(request):
    if request.method == 'POST':
        form = NewSpesaTipo2Form(request.POST)
        form.anno_formativo = request.session['anno_formativo_pk']
        if form.is_valid():
            spesa = form.save(commit=False)
            spesa.anno_formativo = get_anno_formativo(request)
            spesa.save()
            return redirect('acquisti:home')
        else:
            print(form.errors)
    else:
        form = NewSpesaTipo2Form(initial={'aliquota_IVA': 22, 'percentuale_IVA_indetraibile': 0})
    return render(request, 'spese/inserisce_altra_spesa.html', {'spesa': form})


@has_permission_decorator(SiwPermessi.SPESE_INSERISCE_NUOVA)
def inserisce_ordine_a_fornitore(request):
    if request.method == 'POST':
        form = NewSpesaTipo1Form(request.POST)
        print(form)
        form.anno_formativo = request.session['anno_formativo_pk']
        if form.is_valid():
            spesa = form.save(commit=False)
            spesa.anno_formativo = get_anno_formativo(request)
            spesa.save()
            return redirect('acquisti:home')
        else:
            print(form.errors)
    else:
        form = NewSpesaTipo1Form(initial={'aliquota_IVA': 22, 'percentuale_IVA_indetraibile': 0,
                                          'tipo': Spesa.TIPO_ACQUISTO_CON_ORDINE_A_FORNITORE,
                                          'stato': Spesa.STATO_BOZZA})
    return render(request, 'spese/inserisce_ordine_a_fornitore.html', {'spesa': form})
