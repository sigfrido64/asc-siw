# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.http import Http404
from siw.sqlserverinterface import sqlserverinterface
import datetime

# Definizioni dei mesi.
# Uso questo sistema per evitare potezionali problemi di configurazione dei locale nei vari server.
MESI = {'01': 'gennaio', '02': 'febbraio', '03': 'marzo', '04': 'aprile', '05': 'maggio', '06': 'giugno',
        '07': 'luglio', '08': 'agosto', '09': 'settembre', '10': 'ottobre', '11': 'novembre', '12': 'dicembre'}


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


def iscrizione_mdl_fields(matricola, corso, data_stampa):
    """
    Recupera la lista dei campi per la stampa di un iscrizione mdl
    
    :param matricola: La matricola dell'allievo.
    :param corso: Il corso cui è iscritto.
    :param data_stampa: Data della stampa del report.
    :return: Lista di dict con i campi che mi servono per la stampa unione.
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
    
    # Interroga il Data base.
    dati = sqlserverinterface(query)

    # Se non trovo il recordo segnalo not found. E' un'errore perchè nella maschera la selezione è sempre coerente.
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

    return dati


def frequenza_mdl_fields(matricola, corso, data_stampa):
    """
    Recupera la lista dei campi per la stampa di un iscrizione mdl

    :param matricola: La matricola dell'allievo.
    :param corso: Il corso cui è iscritto.
    :param data_stampa : Data della stampa del report.
    :return: Lista di dict con i campi che mi servono per la stampa unione.
    """
    # Compone la query per interrogare il database e la lancia.
    query = "SELECT t2.Cognome AS cognome, t2.Nome AS nome, t2.CF AS cf, " \
            "t4.[Codice Corso] AS cod_corso, t4.Denominazione AS corso, " \
            "t4.[Anno Formativo] AS anno_formativo, " \
            "t4.[Data Inizio Corso] AS data_inizio, t4.[Data Termine Corso] AS data_fine, " \
            "t2.Sesso AS sesso " \
            "FROM [Assocam].[dbo].[Iscrizione ai Corsi] AS t1 " \
            "INNER JOIN [Assocam].[dbo].[Anagrafica Persone] AS t2 " \
            "ON t1.Allievo = t2.[Id Persona] " \
            "INNER JOIN [Assocam].[dbo].[Corsi per Iscrizioni] AS t4 " \
            "ON t1.Corso = t4.[Codice Corso] " \
            "WHERE (t1.[Allievo] = " + str(matricola) + " AND t1.[Corso] = '" + corso + "')"
    
    # Interroga il Data base.
    dati = sqlserverinterface(query)
    
    # Se non trovo il recordo segnalo not found. E' un'errore perchè nella maschera la selezione è sempre coerente.
    if not dati:
        raise Http404(f'Nessun dato trovato con matricola = {matricola} e corso = {corso} !')

    # Inserisce il periodo andando a prendere il nome del mese.
    mese_inizio = datetime.datetime.strftime(dati[0]['data_inizio'], '%m', )
    mese_fine = datetime.datetime.strftime(dati[0]['data_fine'], '%m', )
    dati[0]['periodo'] = MESI[mese_inizio] + ' - ' + MESI[mese_fine]

    # Compone le frasi al maschile o al femminile a seconda del sesso.
    dati[0]['signore'] = 'il signor' if (dati[0]['sesso'] == 'M') else 'la signora'
    dati[0]['iscritto'] = 'iscritto' if (dati[0]['sesso'] == 'M') else 'iscritta'
    
    # Aggiunge la data di stampa
    dati[0]['data_stampa'] = data_stampa
    
    return dati


def frequenza_mdl_gg_fields(matricola, corso, data_stampa):
    """
    Recupera la lista dei campi per la stampa di un iscrizione mdl

    :param matricola: La matricola dell'allievo.
    :param corso: Il corso cui è iscritto.
    :param data_stampa : Data della stampa del report.
    :return: Lista di dict con i campi che mi servono per la stampa unione.
    """
    # Compone la query per interrogare il database e la lancia.
    query = "SELECT t2.Cognome AS cognome, t2.Nome AS nome, t2.CF AS cf, " \
            "t4.[Codice Corso] AS cod_corso, t4.Denominazione AS corso, " \
            "t4.[Anno Formativo] AS anno_formativo, " \
            "t4.[Data Inizio Corso] AS data_inizio, t4.[Data Termine Corso] AS data_fine, " \
            "t2.Sesso AS sesso " \
            "FROM [Assocam].[dbo].[Iscrizione ai Corsi] AS t1 " \
            "INNER JOIN [Assocam].[dbo].[Anagrafica Persone] AS t2 " \
            "ON t1.Allievo = t2.[Id Persona] " \
            "INNER JOIN [Assocam].[dbo].[Corsi per Iscrizioni] AS t4 " \
            "ON t1.Corso = t4.[Codice Corso] " \
            "WHERE (t1.[Allievo] = " + str(matricola) + " AND t1.[Corso] = '" + corso + "')"
    
    # Interroga il Data base.
    dati = sqlserverinterface(query)
    
    # Se non trovo il recordo segnalo not found. E' un'errore perchè nella maschera la selezione è sempre coerente.
    if not dati:
        raise Http404(f'Nessun dato trovato con matricola = {matricola} e corso = {corso} !')
    
    # Inserisce il periodo andando a prendere il nome del mese.
    mese_inizio = datetime.datetime.strftime(dati[0]['data_inizio'], '%m', )
    mese_fine = datetime.datetime.strftime(dati[0]['data_fine'], '%m', )
    dati[0]['periodo'] = MESI[mese_inizio] + ' - ' + MESI[mese_fine]
    
    # Compone le frasi al maschile o al femminile a seconda del sesso.
    dati[0]['signore'] = 'il signor' if (dati[0]['sesso'] == 'M') else 'la signora'
    
    # Aggiunge la data di stampa
    dati[0]['data_stampa'] = data_stampa
    
    return dati

