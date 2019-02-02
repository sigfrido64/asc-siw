# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from accounts.models import SiwPermessi
from siw.decorators import has_permission_decorator
from siw.sig_utils import get_anno_formativo
from .models import AcquistoConOrdine, RipartizioneSpesaPerCDC, somma_delle_ripartizioni
from .forms import NewSpesaTipo2Form, AcquistoConOrdineForm, RipartizioneForm


@has_permission_decorator(SiwPermessi.ACQUISTI_ORDINI_VIEW)
def ordini(request):
    spese = AcquistoConOrdine.objects.filter(anno_formativo=request.session['anno_formativo_pk'])
    spese = spese.order_by('stato', 'data_ordine', 'numero_protocollo')
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
            return redirect('acquisti:inserimento_cdc', pk=ordine.id)
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
            # DOPO aver salvato aggiorno i costi delle ripartizioni.
            ordine.aggiorna_ripartizioni()
            # Se ho tutte le ripartizioni calcolo il costo totale e ritorno alla maschera principale, altrimenti
            # ritorno all'inserimento delle ripartizioni.
            if (somma_delle_ripartizioni(ordine.id, 1)) == 100:
                ordine.calcola_costo_totale()
                return redirect('acquisti:ordini')
            else:
                return redirect('acquisti:inserimento_cdc', pk=ordine.id)
    else:
        form = AcquistoConOrdineForm(instance=ordine)
    return render(request, 'acquisti/inserisce_modifica_ordine.html', {'ordine': form})


@has_permission_decorator(SiwPermessi.ACQUISTI_ORDINI_INSERISCE)
def inserimento_cdc(request, pk):
    ordine = AcquistoConOrdine.objects.get(pk=pk)
    if request.method == 'POST':
        form = RipartizioneForm(request.POST, initial={'acquisto': ordine})
        if form.is_valid():
            form.save()
            if (somma_delle_ripartizioni(ordine.id, 1)) == 100:
                ordine.calcola_costo_totale()
                return redirect('acquisti:ordini')
            else:
                return redirect('acquisti:inserimento_cdc', pk=ordine.id)
    else:
        percentuale_massima_ammissibile = 100 - somma_delle_ripartizioni(ordine.id, 1)
        form = RipartizioneForm(initial={'percentuale_di_competenza': percentuale_massima_ammissibile,
                                         'acquisto': ordine})
    lista_ripartizioni = RipartizioneSpesaPerCDC.objects.filter(acquisto=pk)
    return render(request, 'acquisti/inserisce_ripartizione_su_cdc.html',
                  {'ordine': ordine, 'ripartizione': form, 'lista_ripartizioni': lista_ripartizioni})
