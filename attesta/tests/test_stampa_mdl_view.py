# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.conf import settings
from accounts.models import SiwPermessi
from ..views import stampa_mdl
from os import remove
import shutil
from unipath import Path

__author__ = "Pilone Ing. Sigfrido"


URL = '/attesta/stampe/mdl/iscrizione_mdl/PLCC19/926/12-03-2018/'  # Questo è il link che ho scritto nelle urls per arrivare a questa vista.
REVERSE_URL = 'attesta:stampa_mdl'  # Questa è la stringa che uso per il reverse per vedere che link genera.
# reverse('admin:app_list', kwargs={'app_label': 'auth'})
#  path('stampe/mdl/<str:report>/<str:corso>/<int:matricola>/<str:data_stampa>', views.stampa_mdl, name='stampa_mdl'),

# Percorso dove trovo il report di test.
SOURCE = Path(__file__).parent.parent.child('fixtures').child('test_report_zzz.docx')
# Percorso dove devo mettere il report di test.
DEST = Path(settings.WORD_TEMPLATES).child('mdl').child('test_report_zzz.docx')


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
        shutil.copy(SOURCE, DEST)

    def tearDown(self):
        # Chiusura del test, cancello il report che ho copiato nella posizione di origine.
        # Il file può non esistere per cui uso il try e gestisco eventuale eccezzione.
        try:
            remove(DEST)
        except OSError:
            pass
        
        
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


class ViewSpecificTests(MyAccountTestCase):
    # Qui metto i test specifici della vista per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi e che i permessi risolvano la vista corretta ma nulla più.
    fixtures = ['reports']  # Carico il database di esempio dei report.
    
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
        remove(DEST)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
