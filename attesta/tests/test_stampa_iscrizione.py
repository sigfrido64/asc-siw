# coding=utf-8
from django.urls import reverse
from accounts.models import SiwPermessi
from ..sqlserverdata import iscrizione_mdl_fields
from .test_stampa_mdl_view import MyAccountTestCase, delete
import json
__author__ = "Pilone Ing. Sigfrido"

# Questa è la stringa che uso per il reverse per generare gli url per le prove.
# La sintassi è : reverse('admin:app_list', kwargs={'app_label': 'auth'})
REVERSE_URL = 'attesta:stampa_mdl'


class IscrizioneSpecificTests(MyAccountTestCase):
    # Qui metto i test specifici della vista per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi e che i permessi risolvano la vista corretta ma nulla più.
    
    fixtures = ['reports']  # Carico il database di esempio dei report.
    
    # Dati che mi aspetto in uscita dal controllo dei campi per la stampa unione e che ho generato così :
    # file = open('sig.txt', 'w') | file.write(json.dumps(self.dati, sort_keys=True, indent=4)) | file.close()
    dati_attesi_str = """[
        {
            "cap_res": "10141",
            "cauzione": "Cauzione : 150.00 \u20ac",
            "cf": "CMTNTN55B20H403L",
            "cittadinanza": "Italia",
            "cognome": "Comito",
            "comune_nascita": "Rocca di Neto",
            "comune_res": "Torino",
            "corso": "PLCC19 - PROGETTISTA MECCATRONICO",
            "data_nascita": "20/02/1955",
            "data_stampa": "13/11/1964",
            "indirizzo_res": "Via Tofane, 68",
            "mail": null,
            "nome": "Antonio",
            "occupato": "SI",
            "p_na": "KR",
            "p_res": "TO",
            "sesso": "M",
            "sottoscritto": "Il sottoscritto",
            "stato_nascita": "Italia",
            "telefono": "3356631522",
            "titolo_studio": "Qualifica Professionale Regionale"
        }
    ]"""
    
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)

    def test_incorrect_date_fail(self):
        # Se do una data non valida mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'iscrizione_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '38-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    def test_no_record_allievo_fail(self):
        # Se cerco un record che non esiste mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'iscrizione_mdl', 'corso': 'PLCC00', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_no_file_for_report(self):
        # Se cerco un report che non c'è mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'iscrizione_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        
        # Per fare in modo che non ci sia un report valido lo cancello prima di chiamare la vista.
        delete(self.reportname)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    def test_correct_dict_for_report(self):
        # Controlla che il dizionario che mi viene restituito per la stampa unione sia corretto e contenga tutti i
        # campi che mi servono.
        dati = iscrizione_mdl_fields(926, 'PLCC19', '13/11/1964')
        datiattesi = json.loads(self.dati_attesi_str)
        self.assertEqual(dati, datiattesi)
        
    def test_report_ok(self):
        # Se tutti i dati sono congruenti devo avere una risposta positiva.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'iscrizione_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
