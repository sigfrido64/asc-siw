# coding=utf-8
import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Azienda, Persona, Fornitore
from siw.sqlserverinterface import sqlserverinterface
from .sqlserveranagrafe import QUERY_SELECT_AZIENDE, compila_e_salva_record_azienda
from .sqlserveranagrafe import QUERY_SELECT_PERSONE, compila_e_salva_record_persona
from .sqlserveranagrafe import QUERY_SELECT_CONTATTI_AZIENDE, salva_contatto_azienda_come_persona, \
    salva_contatto_azienda
from celery import shared_task
from siw.context_processor import set_current_username


@shared_task
def allinea_aziende_task(user):
    set_current_username(user)
    # Recupera la lista delle aziende.
    aziende_asc = sqlserverinterface(QUERY_SELECT_AZIENDE)

    count = totali = aggiornati = inseriti = 0
    print("Si parte !")
    for azienda_asc in aziende_asc:
        try:
            azienda = Azienda.objects.get(asc_id=azienda_asc['Id Azienda'])
        except ObjectDoesNotExist:
            compila_e_salva_record_azienda(azienda_asc)
            inseriti += 1
        else:
            if azienda_asc['TsAggiornamento'] > azienda.asc_data_elemento:
                compila_e_salva_record_azienda(azienda_asc, azienda)
                aggiornati += 1

        count = count + 1
        totali = totali + 1
        if count > 50:
            print(__name__ + "Aziende processate altre 50 alle " + datetime.datetime.now().__str__() + " per un totale di " +
                  totali.__str__())
            count = 0

    # Compongo la risposta.
    return f"Allineate Aziende !, processate : {totali}, aggiornate : {aggiornati}, inserite : {inseriti}"


@shared_task
def allinea_persone_task(user):
    set_current_username(user)
    # Recupera la lista delle persone.
    persone_asc = sqlserverinterface(QUERY_SELECT_PERSONE)

    count = totali = aggiornati = inseriti = 0
    print("Si parte !")
    for persona_asc in persone_asc:
        try:
            persona = Persona.objects.get(asc_id=persona_asc['Id Persona'])
        except ObjectDoesNotExist:
            compila_e_salva_record_persona(persona_asc)
            inseriti += 1
        else:
            if persona_asc['Data Elemento'] > persona.asc_data_elemento:
                compila_e_salva_record_persona(persona_asc, persona)
                aggiornati += 1

        count = count + 1
        totali = totali + 1
        if count > 50:
            print(__name__ + "Persone Processate altri 50 alle " + datetime.datetime.now().__str__() + " per un totale di " +
                  totali.__str__())
            count = 0

    # Compongo la risposta.
    return f"Allineate Persone !, processati : {totali}, aggiornati : {aggiornati}, inseriti : {inseriti}"


@shared_task
def allinea_contatti_aziende_task(user):
    set_current_username(user)
    # Vado a leggere gli elementi dal data base SQL Server.
    # query = "SELECT * from [Assocam].[dbo].[Anagrafica Persone] "
    contatti_in_azienda_asc = sqlserverinterface(QUERY_SELECT_CONTATTI_AZIENDE)

    count = totali = aggiornati = inseriti = 0
    print("Si parte !")
    for contatto_in_azienda_asc in contatti_in_azienda_asc:
        try:
            persona = Persona.objects.get(asc_ca_id=contatto_in_azienda_asc['Id Contatto'])
        except ObjectDoesNotExist:
            salva_contatto_azienda_come_persona(contatto_in_azienda_asc)
            persona = Persona.objects.get(asc_ca_id=contatto_in_azienda_asc['Id Contatto'])
            salva_contatto_azienda(contatto_in_azienda_asc, persona)
            inseriti += 1
        else:
            if contatto_in_azienda_asc['TsAggiornamento'] > persona.asc_ca_data_elemento:
                salva_contatto_azienda_come_persona(contatto_in_azienda_asc, persona)
                salva_contatto_azienda(contatto_in_azienda_asc, persona)
                aggiornati += 1

        count = count + 1
        totali = totali + 1
        if count > 50:
            print(__name__ + "Contatti Processati altri 50 alle " + datetime.datetime.now().__str__() + " per un totale di " +
                  totali.__str__())
            count = 0

    # Compongo la risposta.
    return f"Allineato Contatti Aziende !, processati : {totali}, aggiornati : {aggiornati}, inseriti : {inseriti}"
