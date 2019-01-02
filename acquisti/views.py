# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from accounts.models import SiwPermessi
from siw.decorators import has_permission_decorator
from siw.sig_utils import get_anno_formativo
from .models import AcquistoConOrdine
from .forms import NewSpesaTipo2Form, AcquistoConOrdineForm


@has_permission_decorator(SiwPermessi.ACQUISTI_ORDINI_VIEW)
def ordini(request):
    spese = AcquistoConOrdine.objects.filter(anno_formativo=request.session['anno_formativo_pk'])
    return render(request, 'acquisti/ordini.html', {'spese': spese})


def aggiorna_spese(request):
    spese = AcquistoConOrdine.objects.filter(anno_formativo=request.session['anno_formativo_pk'], dirty=True)
    for spesa in spese:
        spesa.calcola_costo_totale()
    return HttpResponse("Fatto !")


@has_permission_decorator(SiwPermessi.ACQUISTI_ORDINI_INSERISCE)
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
    return render(request, 'acquisti/inserisce_altra_spesa.html', {'spesa': form})


@has_permission_decorator(SiwPermessi.ACQUISTI_ORDINI_INSERISCE)
def ordine_inserisce(request):
    if request.method == 'POST':
        form = AcquistoConOrdineForm(request.POST)
        if form.is_valid():
            ordine = form.save(commit=False)
            ordine.anno_formativo = get_anno_formativo(request)
            ordine.save()
            return redirect('acquisti:ordini')
    else:
        form = AcquistoConOrdineForm(initial={'aliquota_IVA': 22, 'percentuale_IVA_indetraibile': 0,
                                              'tipo': AcquistoConOrdine.TIPO_ORDINE_A_FORNITORE,
                                              'stato': AcquistoConOrdine.STATO_BOZZA})
    return render(request, 'acquisti/inserisce_modifica_ordine.html', {'ordine': form})


@has_permission_decorator(SiwPermessi.ACQUISTI_ORDINI_MODIFICA)
def ordine_modifica(request, pk):
    ordine = get_object_or_404(AcquistoConOrdine, pk=pk)
    if request.method == 'POST':
        form = AcquistoConOrdineForm(request.POST, instance=ordine)
        if form.is_valid():
            ordine = form.save(commit=False)
            ordine.anno_formativo = get_anno_formativo(request)
            ordine.save()
            return redirect('acquisti:ordini')
    else:
        form = AcquistoConOrdineForm(instance=ordine)
    return render(request, 'acquisti/inserisce_modifica_ordine.html', {'ordine': form})
