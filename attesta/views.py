# coding=utf-8
from django.shortcuts import render
from siw.sqlserverinterface import sqlserverinterface
from django.http import HttpResponse
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from docxtpl import DocxTemplate
from os import stat
from accounts.models import SiwPermessi
from siw.decorators import has_permission_decorator
from .sqlserverdata import lista_corsi, iscrizione_mdl_fields, frequenza_mdl_fields, frequenza_mdl_gg_fields
from .sqlserverdata import esame_giorni_fields, finale_esame_fields
from .models import Report
from unipath import Path
import tempfile
import datetime
import re
__author__ = "Pilone Ing. Sigfrido"

# Definisco le funzioni per la raccolta dei dati.
# TODO I report dei giorni d'esame sono sostanzialmente unificabili, prima tra qualifica e specializzazione e poi
# TODO tra pre e post esame. Qualifica e specializzazione vengono direttamente dal db. Pre e post esame posso anche
# TODO deciderlo in base alla data di stampa.
dispach_dati_func = {'iscrizione_mdl': iscrizione_mdl_fields,
                     'frequenza_mdl': frequenza_mdl_fields,
                     'frequenza_mdl_gg': frequenza_mdl_gg_fields,
                     'pre_esame_mdl': esame_giorni_fields,
                     'post_esame_mdl': esame_giorni_fields,
                     'finale_esame_mdl': finale_esame_fields
                     }


# Pagina di attestazioni, dichiarazioni ed iscrizioni MDL
@has_permission_decorator(SiwPermessi.STAMPE_MDL)
def mdl(request):
    # Compongo la lista degli anni formativi
    query = "SELECT [Anno Formativo] AS anno from [Assocam].[dbo].[Tabella Anni Formativi] " \
            "ORDER BY [Default] DESC, [Anno Formativo] DESC"
    anni = sqlserverinterface(query)
    
    # Prendo il primo anno per la query che segue.
    anno_default = anni[0].get('anno')
    return render(request, 'attesta/mdl.html', {'anni': anni, 'corsi': lista_corsi(anno_default)})


#
# Sezione Stampe
#
@has_permission_decorator(SiwPermessi.STAMPE_MDL)
def stampa_mdl(request, corso, matricola, reportname, data_stampa):
    """
    Realizza il modulo di iscrizione utilizzando il template previsto.
    
    :param request: Handle della richiesta.
    :param corso: Corso.
    :param matricola: Matricola dell'allievo.
    :param reportname: Nome del report, chiave primaria per il report stesso.
    :param data_stampa: Data di stampa del report.
    :return: Scarica il file con la domanda di iscrizione compilata.

    TODO Refactor delle funzioni javascript che ho nel template. Sono doppie tra scelta documento e cambio data
    """
    # Controllo che la data di stampa sia corretta nel formato GG/MM/AAAA altrimenti segnalo not found.
    data_stampa = check_data_stampa(data_stampa)
   
    # Recupera la lista dei campi che mi servono per la stampa unione usando il dispatch dinamico basato sul nome
    # univoco del report.
    recupera_dati_func = dispach_dati(reportname)
    dati = recupera_dati_func(matricola, corso, data_stampa)

    # Recupera il report richiesto se esiste nel db altrimenti segnala not found !
    report = get_object_or_404(Report, nome=reportname)
    
    # Crea il percorso completo al file di template.
    template = Path(settings.WORD_TEMPLATES).child(report.subfolder).child(report.nome_file)
    # E controlla che il file esista altrimenti segnala not found.
    if not template.exists():
        raise Http404(f'Non trovo il report : {report.nome} in {template}')

    # Crea il nome del file proposto per lo scaricamento come downloadfilename-corso-matricola.
    nomefileoutput = report.downloadfilename + '-' + corso + '-' + str(matricola) + '.docx'
  
    return stampa_unione(template, dati, nomefileoutput)


#
# Sezione procedure di appoggio.
#
def stampa_unione(template, dati, file_out):
    """
    Fa la stampa unione di dati con un template.
    
    La stampa unione la faccio solo con la prima riga della lista. Questa è una scelta perchè voglio stampare
    una dichiarazione per volta.
    
    :param template: Percorso e nome del file di template che contiene il master per la stampa unione.
    :param dati: Lista di dizionari che contengono i dati per la stampa unione e di cui uso solo la prima riga.
    :param file_out: Nome del file che viene proposto per lo scaricamento all'utente.
    :return: Oggetto response che rappresenta il file da scaricare.
    """
    # Crea un percorso completo per un file temporaneo in cui salvare il documento.
    risultato = tempfile.NamedTemporaryFile().name
    
    # Fa il merge con la prima riga della lista e salva il file in uscita temporaneo.
    doc = DocxTemplate(template)
    doc.render(dati[0])
    doc.save(risultato)
    
    # Crea un oggetto response per fare lo scaricamento del file.
    handle = open(risultato, 'rb')
    response = HttpResponse(handle,
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=' + file_out
    response['Content-Length'] = str(stat(risultato).st_size)
    
    return response


def check_data_stampa(data_stampa):
    """
    Controlla che la data_stampa sia valida e la mette nel formato gg/mm/yyyy.
    
    Nel browser uso un controllo che mette la data nella forma gg-mm-yyyy in quanto gli slash andrebbero in
    conflitto con la modalità con cui Django genera i path. Si confonderebbero con ulteriori percorsi.
    Se la stringa non è valida solleva l'eccezione 404 (not found).
    
    :param data_stampa: Stringa che arriva dal browser e che contiene la data stampa nel formato gg-mm-yyyy
    :return: La stessa data sotto forma di stringa nel formato gg/mm/yyyy.
    """
    try:
        data_stampa = datetime.datetime.strptime(data_stampa, '%d-%m-%Y').strftime('%d/%m/%Y')
    except ValueError:
        raise Http404(f'Data di stampa = {data_stampa} invalida !.')
    return data_stampa


def dispach_dati(reportname):
    """
    Dato un nome di report riporta la funzione che si occupa di recuperare i dati per la stampa unione.
    
    Il nome del report determina la funzione con cui recupero i dati considerando la peculiarità che se il
    nome termina con _t[0-9] quella parte non viene considerata in quanto, per convezione, il report non cambia se
    non per elementi testuali interni ma i dati sono gestiti allo stesso identico modo.
    
    :param reportname: Nome del report
    :return: Funzione che recupera il suoi dati per la stampa unione.
    """
    # Come prima cosa elimino eventuali tipologie dal nome del report.
    cleanreport = re.sub(r'_t[0-9]$', '', reportname)
    
    if cleanreport not in dispach_dati_func.keys():
        raise Http404(f'Tipo di report non previsto. Report = {reportname}!.')
    return dispach_dati_func[cleanreport]
