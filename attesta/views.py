# coding=utf-8
from django.shortcuts import render
from siw.sqlserverinterface import sqlserverinterface
from django.http import HttpResponse
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from docxtpl import DocxTemplate
from os import path, stat
from accounts.models import SiwPermessi
from siw.decorators import has_permission_decorator
from .sqlserverdata import lista_corsi
from .models import Report
from unipath import Path
import tempfile
import datetime
__author__ = "Pilone Ing. Sigfrido"


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
    :param request: Handle della richiesta.
    :param corso: Corso.
    :param matricola: Matricola dell'allievo.
    :param reportname: Nome del report, chiave primaria per il report stesso.
    :param data_stampa: Data di stampa del report.
    :return: Scarica il file con la domanda di iscrizione compilata.

    TODO La sottocartella del report deve arrivare dal report stesso
    TODO Refactor delle funzioni javascript che ho nel template. Sono doppie tra scelta documento e cambio data
    TODO Devo mettere il report giusto nella richiesta.
    TODO L'errore dovrebbe essere segnalato alla funzione chiamante in qualche modo.
    """
    # Controllo che la data di stampa sia corretta nel formato GG/MM/AAAA
    try:
        data_stampa = datetime.datetime.strptime(data_stampa, '%d-%m-%Y').strftime('%d/%m/%Y')
    except ValueError:
        raise Http404(f'Data di stampa = {data_stampa} invalida !.')

    # Compone la query per interrogare il database e la lancia.
    query = "SELECT t2.Cognome AS cognome, t2.Nome AS nome, t2.CF AS cf, t2.[Data Nascita] AS data_nascita, " \
            "t2.[Comune Nascita] AS comune_nascita, t2.[Provincia Nascita] AS p_na, " \
            "t2.[Stato Nascita] AS stato_nascita, t2.Cittadinanza AS cittadinanza, " \
            "t2.[Indirizzo Residenza] AS indirizzo_res, t2.[CAP Residenza] AS cap_res, " \
            "t2.[Comune Residenza] AS comune_res, t2.[Provincia Residenza] AS p_res, " \
            "t3.Titolo AS titolo_studio, " \
            "t2.Tel1 AS telefono, t2.Mail1 AS mail, t2.Occupato AS occupato, " \
            "t4.[Codice Corso] + ' - ' + t4.Denominazione AS corso, " \
            "t2.Sesso AS sesso " \
            "FROM [Assocam].[dbo].[Iscrizione ai Corsi] AS t1 " \
            "INNER JOIN [Assocam].[dbo].[Anagrafica Persone] AS t2 " \
            "ON t1.Allievo = t2.[Id Persona] " \
            "INNER JOIN [Assocam].[dbo].[Titoli di Studio] AS t3 " \
            "ON t2.[Titolo Studio] = t3.Codice " \
            "INNER JOIN [Assocam].[dbo].[Corsi per Iscrizioni] AS t4 " \
            "ON t1.Corso = t4.[Codice Corso] " \
            "WHERE (t1.[Allievo] = " + str(matricola) + " AND t1.[Corso] = '" + corso + "')"
    dati = sqlserverinterface(query)

    # Se non trovo nulla segnalo Permission Denied in questa prima fase.
    if not dati:
        raise Http404(f'Nessun dato trovato con matricola = {matricola} e corso = {corso} !')

    # A seconda del sesso aggiunge 'Il sottoscritto' o 'La sottoscritta'
    dati[0]['sottoscritto'] = 'Il sottoscritto' if (dati[0]['sesso'] == 'M') else 'La sottoscritta'
    # Cambia il valore di 'occupato' da booleano a stringa.
    dati[0]['occupato'] = 'SI' if dati[0]['occupato'] else 'NO'
    # Converte la data di nascia nel formato standard GG/MM/YYYY
    dati[0]['data_nascita'] = dati[0]['data_nascita'].strftime('%d/%m/%Y')
    # Aggiunge la data di stampa
    dati[0]['data_stampa'] = data_stampa

    # Controllo che il report richiesto esista sia come record nel database che come file da compilare in stampa.
    # Crea il percorso completo al file di template.
    report = get_object_or_404(Report, nome=reportname)
    
    # template = path.join(settings.WORD_TEMPLATES, report.subfolder, report.nome_file)
    template = Path(settings.WORD_TEMPLATES).child(report.subfolder).child(report.nome_file)
    # Controlla che esista.
    if not template.exists():
        raise Http404(f'Non trovo il report : {report.nome} in {template}')

    # A questo punto ho un record ed una data validi e posso comporre il report.
    # Crea un percorso completo per un file temporaneo in cui salvare il documento.
    risultato = tempfile.NamedTemporaryFile().name
    
    # Fa il merge
    doc = DocxTemplate(template)
    doc.render(dati[0])
    doc.save(risultato)
    
    # Crea il nome del file come iscrizione-corso-matricola.
    nomefile = report.downloadfilename + '-' + corso + '-' + str(matricola) + '.docx'
    
    # Risponde con il download del file
    handle = open(risultato, 'rb')
    response = HttpResponse(handle,
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=' + nomefile
    response['Content-Length'] = str(stat(risultato).st_size)

    return response
