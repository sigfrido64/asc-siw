# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.shortcuts import render
from .sqlserverdata import lista_corsi, lista_allievi
from accounts.models import SiwPermessi
from siw.decorators import ajax_has_permission_decorator
from .models import ReportAssociato, Report

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
    corso = request.GET.get('corso')
    return render(request, 'attesta/allievi_list_table.html', {'allievi': lista_allievi(corso)})


# @ajax_has_permission_decorator(SiwPermessi.STAMPE_MDL)
def ajax_load_reports(request):
    """
    Rimanda in Ajax la lista dei reports associati ad un dato corso.
    TODO : Bisogna loggare gli errori nella ricerca delle entry.
    
    :param request: request handle.
    :return: render HTML per combo box.
    """
    corso = request.GET.get('corso')
    # Prendo la lista dei report associati al corso. In questo modo non ho eccezioni se non c'è.
    reports = ReportAssociato.objects.filter(corso=corso).first()
    context_lista = []
    if reports:
        lista_reports = eval(reports.reports)
        for report in lista_reports:
            report = list(Report.objects.filter(nome=report).values('nome', 'descrizione'))
            if report:
                context_lista += report
    return render(request, 'attesta/reports_list_options.html', {'reports': context_lista})
