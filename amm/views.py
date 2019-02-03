# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models.centri_di_costo import CentroDiCosto
from acquisti.models import RipartizioneSpesaPerCDC

analitico_cdc = dict()


@has_permission_decorator(SiwPermessi.AMM_CDC_READ)
def cdc_home(request):
    return render(request, 'amm/cdc_list.html')


def bollicine(id_nodo):
    # TODO La struttura può essere locale alla vista ?
    # Come gestisco l'aggiornamento bulk di una struttura dati su cui poi vado a vedere i risultati ?
    # Lego un record one_to_one ?
    lista_figli = list()
    for nodo in analitico_cdc:
        f.write(str(nodo) + str(analitico_cdc[nodo]))
        if analitico_cdc[nodo]['parent'] == id_nodo:
            lista_figli.append(nodo)
    if lista_figli:
        f.write('Lista Figli di ' + str(id_nodo) + ' -> ' + str(lista_figli))
        for figlio in lista_figli:
            bollicine(figlio)
        padre = analitico_cdc[id_nodo]['parent']
        if padre > 0:
            analitico_cdc[padre]['costo'] = analitico_cdc[padre]['costo'] + analitico_cdc[id_nodo]['costo']
    else:
        padre = analitico_cdc[id_nodo]['parent']
        analitico_cdc[padre]['costo'] = analitico_cdc[padre]['costo'] + analitico_cdc[id_nodo]['costo']
        
        
def run_analisi(request):
    # Prendo tutti i cdc compresa la radice.
    lista_cdc = CentroDiCosto.objects.filter(Q(root=1) | Q(id=1))
    for cdc in lista_cdc:
        if cdc.parent is None:
            parent_id = -1
        else:
            parent_id = cdc.parent.id
        analitico_cdc[cdc.id] = {'parent': parent_id, 'nome': cdc.nome, 'descrizione': cdc.descrizione, 'costo': 0,
                                 'ricavo': 0}

    # Adesso che ho la lista devo lavorare sulle ripartizioni. # Qui dovrei prendere solo quelle dell'anno formativo
    # cui fa riferimento l'albero dei cdc
    lista_spese = RipartizioneSpesaPerCDC.objects.all()
    for spesa in lista_spese:
        analitico_cdc[spesa.cdc.id]['costo'] = analitico_cdc[spesa.cdc.id]['costo'] + spesa.costo_totale
        
    # Ora devo iniziare a fare i conti con le bolle che risalgono fino alla radice.
    bollicine(1)
    return JsonResponse(analitico_cdc, safe=False)
