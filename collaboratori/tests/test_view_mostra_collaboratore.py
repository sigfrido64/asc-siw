# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import ModelForm
from unittest import skip
from accounts.models import SiwPermessi
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from siw.sig_utils import response_debug

from ..views import mostra_collaboratore_view
__author__ = "Pilone Ing. Sigfrido"


# Url della vista scritto sia in modo diretto che in modo interno.
ID = 1
URL = f"/collaboratori/anagrafica/dettaglio/mostra/{ID}/"
REVERSE_URL = 'collaboratori:mostra_collaboratore'


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL, kwargs={'pk': ID})
        self.assertEquals(url, URL)

    def test_mostra_collaboratore_url_resolves_mostra_collaboratore_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, mostra_collaboratore_view)


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi.
    Metto 'username' e 'passoword' e l'url della pagina che voglio testare come reverse
    """
    fixtures = ['af']
    
    def setUp(self):
        # Fake user
        self.fake_user_username = 'john'
        self.fake_user_password = 'secret123'
        self.user = User.objects.create_user(username=self.fake_user_username, email='john@doe.com',
                                             password=self.fake_user_password)
        # Recupero tutti i Dati dell'utente, serve dopo per aggiungere i permessi.
        self.myuser = User.objects.get(username=self.fake_user_username)


class LoginRequiredTests(MyAccountTestCase):
    def test_redirection_to_login_for_not_logged_in_user(self):
        login_url = reverse('login')
        response = self.client.get(URL)
        self.assertRedirects(response, f'{login_url}?next={URL}')


class PermissionRequiredTests(MyAccountTestCase):
    def test_deny_for_logged_in_user_not_authorized_on_app(self):
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)


class FormGeneralTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['collaboratori', 'af']

    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.COLLABORATORE_MOSTRA}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)

    def test_server_serve_page_without_errors(self):
        self.assertEquals(self.response.status_code, HTTP_200_OK)

    def test_render_with_all_needed_and_correct_templates(self):
        self.assertTemplateUsed(self.response, 'collaboratori/mostra_collaboratore.html')
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'includes/menu.html')

    def test_page_contain_known_collaborator(self):
        self.assertContains(self.response, 'Pace')
        self.assertContains(self.response, 'Gaspare')

    def test_page_not_contains_edit_link_without_permission(self):
        self.assertNotContains(self.response, '/collaboratori/anagrafica/modifica/')


class FormTestsForSpecialPermissions(MyAccountTestCase):
    # Adesso controllo che ci siano i pulsanti che vengono abilitati con permessi speciali.
    fixtures = ['collaboratori', 'af']
    
    def test_page_contains_edit_link_when_allowed(self):
        self.myuser.profile.permessi = {SiwPermessi.COLLABORATORE_MOSTRA, SiwPermessi.COLLABORATORE_MODIFICA}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)
        self.assertContains(self.response, '/collaboratori/anagrafica/modifica/')

    def test_page_contains_show_anagrafica_when_allowed(self):
        self.myuser.profile.permessi = {SiwPermessi.COLLABORATORE_MOSTRA, SiwPermessi.ANAGRAFE_DETTAGLIO_PERSONA_MOSTRA}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)
        self.assertContains(self.response, '/anagrafe/ajax/dettaglio-persona/')
