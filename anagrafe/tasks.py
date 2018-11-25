# coding=utf-8
import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Azienda
from siw.sqlserverinterface import sqlserverinterface
from celery import shared_task


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


@shared_task
def prova(total):
    for i in range(total):
        print("Sono alla : ", str(i))
    return 'Finito !'


@shared_task
def prova_1(total):
    for i in range(total):
        print("Sono alla : ", str(i))
    return 'Finito Prova 1!'


@shared_task
def prova_2(total):
    for i in range(total):
        print("Sono alla : ", str(i))
    return 'Finito Prova2!'


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
    

@shared_task
def allinea_aziende_task():
    # Vado a leggere gli elementi dal data base SQL Server.
    # query = "SELECT * from [Assocam].[dbo].[Anagrafica Aziende] "
    aziende_asc = sqlserverinterface(QUERY_SELECT_AZIENDE)

    count = totali = aggiornati = inseriti = 0
    print("Si parte !")
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
    return f"Allineate Aziende !, processate : {totali}, aggiornate : {aggiornati}, inserite : {inseriti}"
