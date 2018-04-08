# coding=utf-8
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import SiwPermessi
from ..sqlserverdata import iscrizione_mdl_fields, frequenza_mdl_fields, frequenza_mdl_gg_fields, esame_giorni_fields
from ..sqlserverdata import finale_esame_fields
from unipath import Path
from os import remove
import json
import shutil
__author__ = "Pilone Ing. Sigfrido"

# Questa è la stringa che uso per il reverse per generare gli url per le prove.
# La sintassi è : reverse('admin:app_list', kwargs={'app_label': 'auth'})
REVERSE_URL = 'attesta:stampa_mdl'

# Percorso dove trovo il report di test.
SOURCE_PATH = Path(__file__).parent.parent.child('fixtures')
# Percorso dove devo mettere il report di test.
DEST_PATH = Path(settings.WORD_TEMPLATES).child('mdl')


def delete(filename):
    """
    Cancella il file se esiste, altrimenti non fa nulla.

    :param filename: Nome del file da cancellare.
    :return: None
    """
    # Il file può non esistere per cui uso il try e gestisco eventuale eccezzione.
    try:
        remove(DEST_PATH.child(filename))
    except OSError:
        pass


def copyfile(filename):
    """
    Copia il file di nome filename dalla sorgente dei report di test alla destionazione dei report nell'app.

    :param filename: Nome del file da copiare tra i due ambienti.
    :return: None
    """
    shutil.copy(SOURCE_PATH.child(filename), DEST_PATH.child(filename))


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi.
    Metto 'username' e 'passoword' e l'url della pagina che voglio testare come reverse
    """
    fixtures = ['reports']  # Carico il database di esempio dei report.
    
    def setUp(self):
        # Fake user
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Dati dell'utente
        self.myuser = User.objects.get(username=self.username)
        # Do i permessi per l'accesso alla vista e faccio il login.
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        # Link alla vista
        self.url = reverse(REVERSE_URL, kwargs={'reportname': 'iscrizione_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                                'data_stampa': '12-03-2018'})
        # Copio il file del report nella posizione di media.
        copyfile(self.reportname)
    
    def tearDown(self):
        # Chiusura del test, cancello il report che ho copiato nella posizione di origine.
        delete(self.reportname)


class IscrizioneSpecificTests(MyAccountTestCase):
    # Test sulla corretta generazione della domanda di iscrizione.

    # Dati che mi aspetto in uscita dal controllo dei campi per la stampa unione e che ho generato così :
    # file = open('sig.txt', 'w') | file.write(json.dumps(dati, sort_keys=True, indent=4)) | file.close()
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
            "nome": "Antonio",
            "occupato": "SI",
            "p_na": "KR",
            "p_res": "TO",
            "sottoscritto": "Il sottoscritto",
            "stato_nascita": "Italia",
            "telefono": "3356631522",
            "titolo_studio": "Qualifica Professionale Regionale"
        }
    ]"""
    
    def setUp(self):
        # Do il nome del report e lancio il setup della classe generale.
        self.reportname = 'test_report_iscrizione_mdl_zzz.docx'
        super().setUp()

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


class FrequenzaSpecificTests(MyAccountTestCase):
    # Test sulla corretta generazione della dichiarazione di frequenza.
    
    # Dati che mi aspetto in uscita dal controllo dei campi per la stampa unione e che ho generato così :
    # file = open('sig.txt', 'w') | file.write(json.dumps(dati, sort_keys=True, indent=4)) | file.close()
    dati_attesi_str = """[
        {
            "anno_formativo": "2017-2018",
            "cf": "CMTNTN55B20H403L",
            "cod_corso": "PLCC19",
            "cognome": "Comito",
            "corso": "PROGETTISTA MECCATRONICO",
            "data_stampa": "13/11/1964",
            "iscritto": "iscritto",
            "nome": "Antonio",
            "periodo": "ottobre - luglio",
            "signore": "il signor"
        }
    ]"""
    
    def setUp(self):
        # Do il nome del report e lancio il setup della classe generale.
        self.reportname = 'test_report_frequenza_mdl_zzz.docx'
        super().setUp()
    
    def test_incorrect_date_fail(self):
        # Se do una data non valida mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_t1', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '38-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_no_record_allievo_fail(self):
        # Se cerco un record che non esiste mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_t1', 'corso': 'PLCC00', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_no_file_for_report(self):
        # Se cerco un report che non c'è mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_t1', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        
        # Per fare in modo che non ci sia un report valido lo cancello prima di chiamare la vista.
        delete(self.reportname)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    def test_correct_dict_for_report(self):
        # Controlla che il dizionario che mi viene restituito per la stampa unione sia corretto e contenga tutti i
        # campi che mi servono.
        dati = frequenza_mdl_fields(926, 'PLCC19', '13/11/1964')
        datiattesi = json.loads(self.dati_attesi_str)
        self.assertEqual(dati, datiattesi)
    
    def test_report_ok(self):
        # Se tutti i dati sono congruenti devo avere una risposta positiva.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_t1', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class FrequenzaGgSpecificTests(MyAccountTestCase):
    # Test sulla corretta generazione della dichiarazione dei giorni di frequenza al corso.
    
    # Dati che mi aspetto in uscita dal controllo dei campi per la stampa unione e che ho generato così :
    # file = open('sig.txt', 'w') | file.write(json.dumps(dati, sort_keys=True, indent=4)) | file.close()
    dati_attesi_str = """[
        {
            "anno_formativo": "2017-2018",
            "cf": "CMTNTN55B20H403L",
            "cod_corso": "PLCC19",
            "cognome": "Comito",
            "corso": "PROGETTISTA MECCATRONICO",
            "data_stampa": "13/11/1964",
            "nome": "Antonio",
            "periodo": "ottobre - luglio",
            "signore": "il signor"
        }
    ]"""
    
    def setUp(self):
        # Do il nome del report e lancio il setup della classe generale.
        self.reportname = 'test_report_frequenza_mdl_gg_zzz.docx'
        super().setUp()
    
    def test_incorrect_date_fail(self):
        # Se do una data non valida mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_gg', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '38-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_no_record_allievo_fail(self):
        # Se cerco un record che non esiste mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_gg', 'corso': 'PLCC00', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_no_file_for_report(self):
        # Se cerco un report che non c'è mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_gg', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        
        # Per fare in modo che non ci sia un report valido lo cancello prima di chiamare la vista.
        delete(self.reportname)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_correct_dict_for_report(self):
        # Controlla che il dizionario che mi viene restituito per la stampa unione sia corretto e contenga tutti i
        # campi che mi servono.
        dati = frequenza_mdl_gg_fields(926, 'PLCC19', '13/11/1964')
        datiattesi = json.loads(self.dati_attesi_str)
        self.assertEqual(dati, datiattesi)
    
    def test_report_ok(self):
        # Se tutti i dati sono congruenti devo avere una risposta positiva.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_gg', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class EsameGgSpecificTests(MyAccountTestCase):
    # Test sulla corretta generazione della dichiarazione dei giorni di esame (pre e post).
    
    # Dati che mi aspetto in uscita dal controllo dei campi per la stampa unione e che ho generato così :
    # file = open('sig.txt', 'w') | file.write(json.dumps(dati, sort_keys=True, indent=4)) | file.close()
    dati_attesi_str = """[
        {
            "anno_formativo": "2017-2018",
            "cf": "CMTNTN55B20H403L",
            "cod_corso": "PLCC19",
            "cognome": "Comito",
            "corso": "PROGETTISTA MECCATRONICO",
            "data_stampa": "13/11/1964",
            "gg_esame": "23/06/2018 dalle ore 18.00 alle ore 21.00",
            "iscritto": "iscritto",
            "nome": "Antonio",
            "signore": "il signor",
            "tipo_attestato": "specializzazione"
        }
    ]"""
    
    def setUp(self):
        # Do il nome del report e lancio il setup della classe generale.
        self.reportname = 'test_report_gg_esame_mdl_zzz.docx'
        super().setUp()
    
    def test_incorrect_date_fail(self):
        # Se do una data non valida mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'pre_esame_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '38-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_no_record_allievo_fail(self):
        # Se cerco un record che non esiste mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'pre_esame_mdl', 'corso': 'PLCC00', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_no_file_for_report(self):
        # Se cerco un report che non c'è mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'pre_esame_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        
        # Per fare in modo che non ci sia un report valido lo cancello prima di chiamare la vista.
        delete(self.reportname)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_correct_dict_for_report(self):
        # Controlla che il dizionario che mi viene restituito per la stampa unione sia corretto e contenga tutti i
        # campi che mi servono.
        dati = esame_giorni_fields(926, 'PLCC19', '13/11/1964')
        datiattesi = json.loads(self.dati_attesi_str)
        self.assertEqual(dati, datiattesi)

    def test_report_ok(self):
        # Se tutti i dati sono congruenti devo avere una risposta positiva.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'pre_esame_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class FinaleEsameSpecificTests(MyAccountTestCase):
    # Test sulla corretta generazione della dichiarazione finale di esame.
    
    # Dati che mi aspetto in uscita dal controllo dei campi per la stampa unione e che ho generato così :
    # file = open('sig.txt', 'w') | file.write(json.dumps(dati, sort_keys=True, indent=4)) | file.close()
    dati_attesi_str = """[
        {
            "anno_formativo": "2017-2018",
            "cf": "CMTNTN55B20H403L",
            "cod_corso": "PLCC19",
            "cognome": "Comito",
            "corso": "PROGETTISTA MECCATRONICO",
            "data_stampa": "13/11/1964",
            "giudizio_finale": "NON IDONEO",
            "iscritto": "iscritto",
            "nome": "Antonio",
            "ore_corso_svolte": "0.0",
            "ore_totali": "0.0",
            "signore": "il signor",
            "tipo_attestato": "specializzazione",
            "valutazione_finale": "0.0"
        }
    ]"""
    
    def setUp(self):
        # Do il nome del report e lancio il setup della classe generale.
        self.reportname = 'test_report_finale_esame_mdl_zzz.docx'
        super().setUp()
    
    def test_incorrect_date_fail(self):
        # Se do una data non valida mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'finale_esame_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '38-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_no_record_allievo_fail(self):
        # Se cerco un record che non esiste mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'finale_esame_mdl', 'corso': 'PLCC00', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_no_file_for_report(self):
        # Se cerco un report che non c'è mi deve dare errore.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'finale_esame_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        
        # Per fare in modo che non ci sia un report valido lo cancello prima di chiamare la vista.
        delete(self.reportname)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    def test_correct_dict_for_report(self):
        # Controlla che il dizionario che mi viene restituito per la stampa unione sia corretto e contenga tutti i
        # campi che mi servono.
        dati = finale_esame_fields(926, 'PLCC19', '13/11/1964')
        datiattesi = json.loads(self.dati_attesi_str)
        file = open('sig.txt', 'w')
        file.write(json.dumps(dati, sort_keys=True, indent=4))
        file.close()
        self.assertEqual(dati, datiattesi)
    
    def test_report_ok(self):
        # Se tutti i dati sono congruenti devo avere una risposta positiva.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'finale_esame_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
