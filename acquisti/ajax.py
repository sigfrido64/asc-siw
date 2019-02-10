# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from siw.sig_utils import from_choices_to_list
from siw.decorators import ajax_has_permission_decorator
from accounts.models import SiwPermessi
from anagrafe.models import Fornitore
from .models import AcquistoConOrdine, RipartizioneSpesaPerCDC, RipartizioneAcquistoWebPerCDC


@login_required()
def ajax_lista_stati_ordine(request):
    return from_choices_to_list(AcquistoConOrdine.STATO_ORDINE_CHOICES)


@login_required()
def ajax_lista_tipo_spesa_2(request):
    lista = list()
    for tipo in AcquistoConOrdine.STATO_ORDINE_CHOICES:
        if 100 < tipo[0] < 300:
            lista.append(tipo)
    return from_choices_to_list(lista)


@login_required()
def ajax_lista_tipo_ordini(request):
    return from_choices_to_list(AcquistoConOrdine.TIPO_ORDINE_CHOICES)


@login_required()
def ajax_lista_fornitori(request):
    # TODO mettere i test e verificare che siano in ordine alfabetico.
    fornitori = Fornitore.objects.filter(in_uso=True).order_by('azienda__ragione_sociale')
    fornitori = fornitori.values('azienda__ragione_sociale', 'pk')
    # Per convertire in Json devo prima convertire in lista.
    fornitori_list = list(fornitori)
    return JsonResponse(fornitori_list, safe=False)


@ajax_has_permission_decorator(SiwPermessi.ACQUISTI_CDC_ERASE)
def ajax_elimina_ripartizione_su_cdc(request, pk):
    ripartizione = get_object_or_404(RipartizioneSpesaPerCDC, id=pk)
    acquisto = ripartizione.acquisto
    ripartizione.delete()
    acquisto.calcola_costo_totale()
    return JsonResponse({'risultato': 'ok'}, safe=False)


@ajax_has_permission_decorator(SiwPermessi.ACQUISTI_CDC_ERASE)
def ajax_elimina_ripartizione_su_cdc_web(request, pk):
    ripartizione = get_object_or_404(RipartizioneAcquistoWebPerCDC, id=pk)
    acquisto = ripartizione.acquisto_web
    ripartizione.delete()
    acquisto.calcola_costo_totale()
    return JsonResponse({'risultato': 'ok'}, safe=False)


@ajax_has_permission_decorator(SiwPermessi.ACQUISTI_ORDINI_VIEW)
def ajax_lista_ripartizioni_per_ordine(request, pk):
    lista_ripartizioni = RipartizioneSpesaPerCDC.objects.filter(acquisto=pk)
    risposta = render_to_string('acquisti/includes/lista_ripartizioni.html', {'lista_ripartizioni': lista_ripartizioni},
                                request)
    return JsonResponse({'html': risposta}, safe=False)


@ajax_has_permission_decorator(SiwPermessi.ACQUISTI_ORDINI_VIEW)
def ajax_lista_ripartizioni_per_ordine_web(request, pk):
    lista_ripartizioni = RipartizioneAcquistoWebPerCDC.objects.filter(acquisto_web=pk)
    risposta = render_to_string('acquisti/includes/lista_ripartizioni.html', {'lista_ripartizioni': lista_ripartizioni},
                                request)
    return JsonResponse({'html': risposta}, safe=False)
