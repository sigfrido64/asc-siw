# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.conf import settings
from accounts.models import SiwPermessi
from ..views import stampa_mdl
from ..sqlserverdata import iscrizione_mdl_fields
from os import remove
import shutil
from unipath import Path
import json
__author__ = "Pilone Ing. Sigfrido"


URL = '/attesta/stampe/mdl/iscrizione_mdl/PLCC19/926/12-03-2018/'  # Questo è il link che ho scritto nelle urls per arrivare a questa vista.
REVERSE_URL = 'attesta:stampa_mdl'  # Questa è la stringa che uso per il reverse per vedere che link genera.
# reverse('admin:app_list', kwargs={'app_label': 'auth'})
#  path('stampe/mdl/<str:report>/<str:corso>/<int:matricola>/<str:data_stampa>', views.stampa_mdl, name='stampa_mdl'),

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
    def setUp(self):
        # Fake user
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Dati dell'utente
        self.myuser = User.objects.get(username=self.username)
        # Link alla vista
        self.url = reverse(REVERSE_URL, kwargs={'reportname': 'iscrizione_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                                'data_stampa': '12-03-2018'})
        # Copio il file del report nella posizione di media.
        self.reportname = 'test_report_iscrizione_mdl_zzz.docx'
        copyfile(self.reportname)

    def tearDown(self):
        # Chiusura del test, cancello il report che ho copiato nella posizione di origine.
        delete(self.reportname)
        
        
class LoginRequiredTests(MyAccountTestCase):
    # Test che faccio per un utente non loggato, un utente guest.
    def test_redirection(self):
        # Un utente non loggato deve essere rediretto alla pagina di login.
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class PermissionRequiredTests(MyAccountTestCase):
    # Qui metto i test per un utente che si logga ma che non ha i permessi per accedere all'app.
    def test_no_perms_on_app(self):
        # Un utente che si logga senza permessi e prova ad accere alla pagina dell'applicazione deve ricevere
        # come risposta 403 = Denied !
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 403)


class ViewGenericTests(MyAccountTestCase):
    # Qui metto i test generali per l'accesso e la risoluzione della vista per un utente che si logga e che ha i
    # permessi per accedere.
    fixtures = ['reports']  # Carico il database di esempio dei report.
    
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        # Il server riesce a fornire la pagina richiesta.
        # Attenzione che la pagina richiesta in realtà è il download di un file.
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)
        
    def test_url_resolves_correct_view(self):
        # La risoluzione dell'url mi manda alla vista corretta.
        # Il test fallisce quando il link non mi porta alla vista e devi guardare negli urls dell'app.
        view = resolve(self.url)
        self.assertEquals(view.func, stampa_mdl)


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


class FrequenzaSpecificTests(TestCase):
    # Qui metto i test specifici della vista per il report della dichiarazione di frequenza.
    # Non uso MyAccountTestCase in quanto le operazioni sono speciali e non serve copiare sempre anche il report
    # di iscrizione.
    fixtures = ['reports']  # Carico il database di esempio dei report.
    
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Recupera i dati dell'utente e gli aggiunge i permessi specifici per la vista.
        self.myuser = User.objects.get(username=self.username)
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        # Infine copia il report di test
        self.reportname = 'test_report_frequenza_mdl_zzz.docx'
        copyfile(self.reportname)

    def tearDown(self):
        # Chiusura del test, cancello il report che ho copiato nella posizione di origine.
        delete(self.reportname)

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
    
    def test_report_ok(self):
        # Se tutti i dati sono congruenti devo avere una risposta positiva.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_t1', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class FrequenzaGgSpecificTests(TestCase):
    # Qui metto i test specifici della vista per il report della dichiarazione di frequenza.
    # Non uso MyAccountTestCase in quanto le operazioni sono speciali e non serve copiare sempre anche il report
    # di iscrizione.
    fixtures = ['reports']  # Carico il database di esempio dei report.
    
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Recupera i dati dell'utente e gli aggiunge i permessi specifici per la vista.
        self.myuser = User.objects.get(username=self.username)
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        # Infine copia il report di test
        self.reportname = 'test_report_frequenza_mdl_gg_zzz.docx'
        copyfile(self.reportname)
    
    def tearDown(self):
        # Chiusura del test, cancello il report che ho copiato nella posizione di origine.
        delete(self.reportname)
    
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
    
    def test_report_ok(self):
        # Se tutti i dati sono congruenti devo avere una risposta positiva.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'frequenza_mdl_gg', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class EsameGgSpecificTests(TestCase):
    # Qui metto i test specifici della vista per TUTTI i report che dichiarano i giorni d'esame. Che sia prima o dopo
    # l'esame e che sia per corsi di qualifica o specializzazione in quanto i report usano gli stessi campi.
    # Non uso MyAccountTestCase in quanto le operazioni sono speciali e non serve copiare sempre anche il report
    # di iscrizione.
    fixtures = ['reports']  # Carico il database di esempio dei report.
    
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Recupera i dati dell'utente e gli aggiunge i permessi specifici per la vista.
        self.myuser = User.objects.get(username=self.username)
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        # Infine copia il report di test
        self.reportname = 'test_report_pre_esame_mdl_zzz.docx'
        copyfile(self.reportname)
    
    def tearDown(self):
        # Chiusura del test, cancello il report che ho copiato nella posizione di origine.
        delete(self.reportname)
    
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
    
    def test_report_ok(self):
        # Se tutti i dati sono congruenti devo avere una risposta positiva.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'pre_esame_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class FinaleEsameSpecificTests(TestCase):
    # Qui metto i test specifici della vista per il report che stampa la dichiarazione finale d'esame con voti e
    # giudizio.
    # Non uso MyAccountTestCase in quanto le operazioni sono speciali e non serve copiare sempre anche il report
    # di iscrizione.
    fixtures = ['reports']  # Carico il database di esempio dei report.
    
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Recupera i dati dell'utente e gli aggiunge i permessi specifici per la vista.
        self.myuser = User.objects.get(username=self.username)
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        # Infine copia il report di test
        self.reportname = 'test_report_finale_esame_mdl_zzz.docx'
        copyfile(self.reportname)
    
    def tearDown(self):
        # Chiusura del test, cancello il report che ho copiato nella posizione di origine.
        delete(self.reportname)
    
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
    
    def test_report_ok(self):
        # Se tutti i dati sono congruenti devo avere una risposta positiva.
        url = reverse(REVERSE_URL, kwargs={'reportname': 'finale_esame_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                           'data_stampa': '12-03-2018'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
