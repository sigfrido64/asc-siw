# encoding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from siw.sqlserverinterface import sqlserverinterface
from django.http import HttpResponse
from django.conf import settings
from docxtpl import DocxTemplate
from unipath import Path
from os import path, stat
import tempfile


#
# Sezioni comuni
#
def lista_corsi(anno):
    """
    Recupera la lista dei corsi MDL per un dato anno formativo.
    :param anno: Anno formativo
    :return: Lista dei corsi di quell'anno formativo.
    """
    query = "SELECT [Codice Corso] AS corso, [Codice Corso] + ' - ' + [Denominazione] AS denominazione " \
            "FROM [Assocam].[dbo].[Corsi per Iscrizioni] " \
            "WHERE [Anno Formativo] = '" + anno + "' AND Tipo <= 2 " \
            "ORDER BY [Codice Corso]"
    return sqlserverinterface(query)
    

def lista_allievi(corso):
    """
    Recupera la lista degli allievi di un dato corso.
    :param corso : Codice corso con edizione.
    :return: Lista degli allievi di quel corso.
    """
    query = "SELECT Cognome AS cognome, Nome AS nome, Corso AS corso, Allievo AS matricola " \
            "FROM [Assocam].[dbo].[Anagrafica Persone] " \
            "INNER JOIN [Iscrizione ai Corsi] ON [Anagrafica Persone].[Id Persona] = [Iscrizione ai Corsi].Allievo " \
            "WHERE ([Iscrizione ai Corsi].Corso = '" + corso + "') " \
            "ORDER BY COGNOME"
    return sqlserverinterface(query)


# Pagina di attestazioni, dichiarazioni ed iscrizioni MDL
@login_required()
def mdl(request):
    # Compongo la lista degli anni formativi
    query = "SELECT [Anno Formativo] AS anno from [Assocam].[dbo].[Tabella Anni Formativi] " \
            "ORDER BY [Default] DESC, [Anno Formativo] DESC"
    anni = sqlserverinterface(query)
    
    # Prendo il primo anno per la query che segue.
    anno_default = anni[0].get('anno')
    return render(request, 'attesta/mdl.html', {'anni': anni, 'corsi': lista_corsi(anno_default)})


#
# Sezione Ajax
#
def load_corsi(request):
    """
    Rimanda in Ajax la lista dei corsi per un dato anno formativo.
    :param request: request handle.
    :return: render HTML per combo box.
    """
    anno = request.GET.get('anno')
    return render(request, 'attesta/corsi_list_options.html', {'corsi': lista_corsi(anno)})


def load_allievi(request):
    """
    Rimanda in Ajax la lista degli allievi di un dato corso.
    :param request: request handle.
    :return: render HTML per tabella.
    """
    corso = request.GET.get('corso')
    return render(request, 'attesta/allievi_list_table.html', {'allievi': lista_allievi(corso)})


#
# Sezione Stampe
#
def stampa_mdl_iscrizione(request, corso, matricola):
    """
    :param request: Handle della richiesta.
    :param corso: Corso.
    :param matricola: Matricola dell'allievo.
    :return: Scarica il file con la domanda di iscrizione compilata.
    """
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
    
    # A seconda del sesso aggiunge 'Il sottoscritto' o 'La sottoscritta'
    dati[0]['sottoscritto'] = 'Il sottoscritto' if (dati[0]['sesso'] == 'M') else 'La sottoscritta'
    
    # Cambia il valore di 'occupato' da booleano a stringa.
    dati[0]['occupato'] = 'SI' if dati[0]['occupato'] else 'NO'
    
    # Converte la data di nascia nel formato standard GG/MM/YYYY
    dati[0]['data_nascita'] = dati[0]['data_nascita'].strftime('%d/%m/%Y')
    
    print(dati)

    print(settings.WORD_TEMPLATES)
    # Crea il percorso completo al file di template.
    template = path.join(settings.WORD_TEMPLATES, 'iscrizione_MDL.docx')
    print(template)
    
    # Crea un percorso completo per un file temporaneo in cui salvare il documento.
    risultato = tempfile.NamedTemporaryFile().name
    print(risultato)
    
    # Fa il merge
    doc = DocxTemplate(template)
    doc.render(dati[0])
    doc.save(risultato)
    
    # Crea il nome del file come iscrizione-corso-matricola.
    nomefile = 'Iscrizione-' + corso + '-' + str(matricola) + '.docx'
    
    # Risponde con il download del file
    handle = open(risultato, 'rb')
    response = HttpResponse(handle,
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=' + nomefile
    response['Content-Length'] = str(stat(risultato).st_size)

    return response
