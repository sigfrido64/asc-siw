# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import SiwPermessi
from amm.views import cdc
__author__ = "Pilone Ing. Sigfrido"


URL = '/amm/cdc/'  # Questo è il link che ho scritto nelle urls per arrivare a questa vista.
REVERSE_URL = 'amm:cdc_home'  # Questa è la stringa che uso per il reverse per vedere che link genera.


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
        self.url = reverse(REVERSE_URL)


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
        

class FormGeneralTests(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.AMM_CDC_READ}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        # Il server riesce a fornire la pagina richiesta.
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_cdc_view(self):
        # La risoluzione dell'url mi manda alla vista corretta.
        # Il test fallisce quando il link non mi porta alla vista e devi guardare negli urls dell'app.
        view = resolve(URL)
        self.assertEquals(view.func, cdc)
        
    def test_use_correct_template(self):
        # Controllo che usi il template corretto.
        self.assertTemplateUsed(self.response, 'amm/cdc_list.html',
                                "Non è stato usato il template corretto")
