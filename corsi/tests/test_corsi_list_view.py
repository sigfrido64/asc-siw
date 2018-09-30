# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import SiwPermessi
from corsi.views import corsi_list_home
__author__ = "Pilone Ing. Sigfrido"


URL = '/corsi/lista/'  # Questo è il link che ho scritto nelle urls per arrivare a questa vista.
REVERSE_URL = 'corsi:home'  # Questa è la stringa che uso per il reverse per vedere che link genera.


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL)
        self.assertEquals(url, URL)

    def test_list_corsi_url_resolves_corsi_list_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, corsi_list_home)


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
    # Un utente non loggato deve essere rediretto alla pagina di login.
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class PermissionRequiredTests(MyAccountTestCase):
    # Un utente che si logga senza permessi e prova ad accere alla pagina dell'applicazione deve ricevere
    # come risposta 403 = Denied !
    def test_no_perms_on_app(self):
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 403)
        

class FormGeneralTests(MyAccountTestCase):
    # Utente che si logga e che ha i permessi per accedere in lettura.
    fixtures = ['cdc.json', 'corsi.json']
    
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.CORSI_LISTA_READ}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        # Il server riesce a fornire la pagina richiesta.
        self.assertEquals(self.response.status_code, 200)
        
    def test_use_correct_template(self):
        # Controllo che usi il template corretto.
        self.assertTemplateUsed(self.response, 'corsi/lista_corsi.html',
                                "Non è stato usato il template corretto")

    def test_find_know_fields_and_data_but_no_detail_link(self):
        utf8_content = self.response.content.decode('utf8')
        expected_html = """
          <tr>
            <td>LIIV08</td>
            <td>Lingua Inglese - Livello Elementare</td>
            <td>60,0</td>
            <td>
              <i class="fa fa-id-card" aria-hidden="true"></i>
            </td>
          </tr>
        """
        self.assertInHTML(expected_html, utf8_content)

    def test_find_know_fields_and_data_but_and_detail_link_when_allowed(self):
        self.myuser.profile.permessi = {SiwPermessi.CORSI_LISTA_READ, SiwPermessi.CORSI_MOSTRA}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(URL)
        self.assertContains(self.response, '/corsi/dettaglio/LIIV08/')
