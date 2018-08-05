# coding=utf-8
import time
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Persona
from siw.sqlserverinterface import sqlserverinterface


# Create your views here.
def vista1(request):
    # Compongo la lista degli anni formativi
    query = """
    SELECT 
      [Id Persona]
      ,[Cognome]
      ,[Nome]
      ,[Data Nascita]
      ,[Stato Nascita]
      ,[Cittadinanza]
      ,[Comune Nascita]
      ,[Provincia Nascita]
      ,[Sesso]
      ,[Indirizzo Domicilio]
      ,[Comune Domicilio]
      ,[CAP Domicilio]
      ,[Provincia Domicilio]
      ,[Indirizzo Residenza]
      ,[Comune Residenza]
      ,[CAP Residenza]
      ,[Provincia Residenza]
      ,[CF]
      ,[PIVA]
      ,[Tel1]
      ,[Tel2]
      ,[Tel3]
      ,[Tel4]
      ,[DTel1]
      ,[DTel2]
      ,[DTel3]
      ,[DTel4]
      ,[Mail1]
      ,[Mail2]
      ,[Titolo Studio]
      ,[Anno Titolo Studio]
      ,[Occupato]
      ,[Data Occupazione]
      ,[Mansioni]
      ,[Ditta]
      ,[Mesi Ricerca Lavoro]
      ,[Studente]
      ,[Docente]
      ,[Data Elemento]
  FROM [Assocam].[dbo].[Anagrafica Persone]
    """
    # query = "SELECT * from [Assocam].[dbo].[Anagrafica Persone] "
    persone_asc = sqlserverinterface(query)

    """
    L'elemento esite già ?
    No : lo inserisco e basta
    
    si : è più nuovo qui di quanto lo ho caricato ?
        si : lo aggiorno
        no : non faccio nulla
        
    """

    count = 0
    totali = 0
    for persona_asc in persone_asc:
        persona = Persona()

        # Sezione ID
        persona.asc_id = persona_asc['Id Persona']
        persona.asc_data_elemento = persona_asc['Data Elemento']
        persona.asc_data_aggiornamento = datetime.datetime.now()

        # Dati personali
        persona.nome = persona_asc['Nome']
        persona.cognome = persona_asc['Cognome']

        # Luogo e data di nascita, Sesso
        persona.comune_nascita = persona_asc['Comune Nascita'] or ''
        persona.provincia_nascita = persona_asc['Provincia Nascita'] or ''
        persona.stato_nascita = persona_asc['Stato Nascita'] or ''
        persona.data_nascita = persona_asc['Data Nascita'] or ''
        persona.sesso = persona_asc['Sesso']

        # Domicilio.
        persona.indirizzo_domicilio = persona_asc['Indirizzo Domicilio'] or ''
        persona.comune_domicilio = persona_asc['Comune Domicilio'] or ''
        persona.cap_domicilio = persona_asc['CAP Domicilio'] or ''
        persona.provincia_domicilio = persona_asc['Provincia Domicilio'] or ''

        # Residenza.
        persona.indirizzo_residenza = persona_asc['Indirizzo Residenza'] or ''
        persona.comune_residenza = persona_asc['Comune Residenza'] or ''
        persona.cap_residenza = persona_asc['CAP Residenza'] or ''
        persona.provincia_residenza = persona_asc['Provincia Residenza'] or ''

        # Codice Fiscale.
        persona.cf = persona_asc['CF'] or ''

        # Recapiti telefonici.
        persona.tel1 = persona_asc['Tel1'] or ''
        persona.tel2 = persona_asc['Tel2'] or ''
        persona.tel3 = persona_asc['Tel3'] or ''
        persona.tel4 = persona_asc['Tel4'] or ''

        persona.doc_tel1 = persona_asc['DTel1'] or ''
        persona.doc_tel2 = persona_asc['DTel2'] or ''
        persona.doc_tel3 = persona_asc['DTel3'] or ''
        persona.doc_tel4 = persona_asc['DTel4'] or ''

        # Posta elettronica.
        persona.mail1 = persona_asc['Mail1'] or ''
        persona.mail2 = persona_asc['Mail2'] or ''

        persona.save()
        count = count + 1
        totali = totali + 1
        if count > 10:
            print(__name__ + "Processati altri 10 alle " + datetime.datetime.now().__str__() + " per un totale di " +
                  totali.__str__())
            count = 0

    # Prendo il primo anno per la query che segue.
    return HttpResponse("Fatto !")
