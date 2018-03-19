# coding=utf-8
from django.shortcuts import render
from .sqlserverdata import lista_corsi, lista_allievi
from accounts.models import SiwPermessi
from siw.decorators import ajax_has_permission_decorator
from .models import ReportAssociato

__author__ = "Pilone Ing. Sigfrido"

#
# Sezione Ajax
#


@ajax_has_permission_decorator(SiwPermessi.STAMPE_MDL)
def ajax_load_corsi(request):
    """
    Rimanda in Ajax la lista dei corsi per un dato anno formativo.
    :param request: request handle.
    :return: render HTML per combo box.
    """
    anno = request.GET.get('anno')
    return render(request, 'attesta/corsi_list_options.html', {'corsi': lista_corsi(anno)})


@ajax_has_permission_decorator(SiwPermessi.STAMPE_MDL)
def ajax_load_allievi(request):
    """
    Rimanda in Ajax la lista degli allievi di un dato corso.
    :param request: request handle.
    :return: render HTML per tabella.
    """
    # Recupero i parametri di GET
    corso = request.GET.get('corso')
    report = request.GET.get('report')
    data_stampa = request.GET.get('data')
    return render(request, 'attesta/allievi_list_table.html', {'allievi': lista_allievi(corso), 'report': report,
                                                               'data_stampa': data_stampa})


@ajax_has_permission_decorator(SiwPermessi.STAMPE_MDL)
def ajax_load_reports(request):
    """
    Rimanda in Ajax la lista dei reports associati ad un dato corso.
    TODO : Bisogna loggare gli errori di ricerca per sapere se qualcuno ha fatto il furbo.
    
    :param request: request handle.
    :return: render HTML per combo box.
    """
    corso = request.GET.get('corso')
    # Prendo la lista dei report associati al corso. In questo modo non ho eccezioni se non c'è.
    return render(request, 'attesta/reports_list_options.html',
                  {'reports': ReportAssociato.lista_report_associati(corso)})
