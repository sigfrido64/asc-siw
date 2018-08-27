# coding=utf-8
import time
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Persona, Azienda
from siw.sqlserverinterface import sqlserverinterface


QUERY_SELECT_PERSONE = """
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

QUERY_SELECT_AZIENDE = """
SELECT [Id Azienda]
      ,[Ragione Sociale]
      ,[Descrizione]
      ,[Indirizzo]
      ,[Città]
      ,[Provincia]
      ,[CAP]
      ,[PIVA]
      ,[CF]
      ,[Tel1]
      ,[Tel2]
      ,[Tel3]
      ,[Tel4]
      ,[DTel1]
      ,[DTel2]
      ,[DTel3]
      ,[DTel4]
      ,[SitoWeb]
      ,[Note]
      ,[HashRagioneSociale]
      ,[Valido]
      ,[Accetta_Promozioni]
      ,[Mail-Azienda]
      ,[TsAggiornamento]
  FROM [dbo].[Anagrafica Aziende]
"""


def _compila_e_salva_record_persona(persona_asc, persona=None):
    if not persona:
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

    # Salva il record.
    persona.save()


def _compila_e_salva_record_azienda(azienda_asc, azienda=None):
    if not azienda:
        azienda = Azienda()

    azienda.asc_id = azienda_asc['Id Azienda']
    azienda.asc_data_elemento = azienda_asc['TsAggiornamento']
    azienda.asc_data_aggiornamento = datetime.datetime.now()

    azienda.ragione_sociale = azienda_asc['Ragione Sociale']
    azienda.descrizione = azienda_asc['Descrizione'] or ''

    azienda.indirizzo = azienda_asc['Indirizzo'] or ''
    azienda.comune = azienda_asc['Città'] or ''
    azienda.cap = azienda_asc['CAP'] or ''
    azienda.provincia = azienda_asc['Provincia'] or ''

    azienda.cf = azienda_asc['CF'] or ''
    azienda.piva = azienda_asc['PIVA'] or ''

    azienda.tel1 = azienda_asc['Tel1'] or ''
    azienda.tel2 = azienda_asc['Tel2'] or ''
    azienda.tel3 = azienda_asc['Tel3'] or ''
    azienda.tel4 = azienda_asc['Tel4'] or ''

    azienda.doc_tel1 = azienda_asc['DTel1'] or ''
    azienda.doc_tel2 = azienda_asc['DTel2'] or ''
    azienda.doc_tel3 = azienda_asc['DTel3'] or ''
    azienda.doc_tel4 = azienda_asc['DTel4'] or ''

    azienda.mail1 = azienda_asc['Mail-Azienda'] or ''

    azienda.sito_web = azienda_asc['SitoWeb'] or ''
    azienda.hashragionesociale = azienda_asc['HashRagioneSociale'] or ''

    # Privacy
    azienda.accetta_promozioni = azienda_asc['Accetta_Promozioni']

    azienda.note = azienda_asc['Note'] or ''
    azienda.in_uso = azienda_asc['Valido']

    # Salva il record.
    azienda.save()


def allinea_persone_view(request):
    # Vado a leggere gli elementi dal data base SQL Server.
    # query = "SELECT * from [Assocam].[dbo].[Anagrafica Persone] "
    persone_asc = sqlserverinterface(QUERY_SELECT_PERSONE)

    count = totali = aggiornati = inseriti = 0
    for persona_asc in persone_asc:
        try:
            persona = Persona.objects.get(asc_id=persona_asc['Id Persona'])
        except ObjectDoesNotExist:
            _compila_e_salva_record_persona(persona_asc)
            inseriti += 1
        else:
            if persona_asc['Data Elemento'] > persona.asc_data_elemento:
                _compila_e_salva_record_persona(persona_asc, persona)
                aggiornati += 1

        count = count + 1
        totali = totali + 1
        if count > 50:
            print(__name__ + "Processati altri 50 alle " + datetime.datetime.now().__str__() + " per un totale di " +
                  totali.__str__())
            count = 0

    # Compongo la risposta.
    return HttpResponse(f"Fatto !, aggiornati : {aggiornati}, inseriti : {inseriti}")


def allinea_aziende_view(request):
    # Vado a leggere gli elementi dal data base SQL Server.
    # query = "SELECT * from [Assocam].[dbo].[Anagrafica Aziende] "
    aziende_asc = sqlserverinterface(QUERY_SELECT_AZIENDE)

    count = totali = aggiornati = inseriti = 0
    for azienda_asc in aziende_asc:
        try:
            azienda = Azienda.objects.get(asc_id=azienda_asc['Id Azienda'])
        except ObjectDoesNotExist:
            _compila_e_salva_record_azienda(azienda_asc)
            inseriti += 1
        else:
            if azienda_asc['TsAggiornamento'] > azienda.asc_data_elemento:
                _compila_e_salva_record_azienda(azienda_asc, azienda)
                aggiornati += 1

        count = count + 1
        totali = totali + 1
        if count > 50:
            print(__name__ + "Processate altre 50 alle " + datetime.datetime.now().__str__() + " per un totale di " +
                  totali.__str__())
            count = 0

    # Compongo la risposta.
    return HttpResponse(f"Fatto !, aggiornate : {aggiornati}, inserite : {inseriti}")
