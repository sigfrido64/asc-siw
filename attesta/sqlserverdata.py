# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.shortcuts import render
from siw.sqlserverinterface import sqlserverinterface


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
