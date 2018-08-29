# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import ModelForm
from unittest import skip
from accounts.models import SiwPermessi
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from siw.sig_debug import response_debug

from ..views import lista_collaboratori_view
__author__ = "Pilone Ing. Sigfrido"


# Url della vista scritto sia in modo diretto che in modo interno.
URL = "/collaboratori/anagrafica/lista/"
REVERSE_URL = 'collaboratori:lista_collaboratori'


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL)
        self.assertEquals(url, URL)

    def test_lista_collaboratori_url_resolves_lista_collaboratori_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, lista_collaboratori_view)


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi.
    Metto 'username' e 'passoword' e l'url della pagina che voglio testare come reverse
    """
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


class FormGeneralTestsForLoggedInUsersWithPermissionsJustForList(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['collaboratori.json']

    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.COLLABORATORI_LISTA_READ}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)

    def test_server_serve_page_without_errors(self):
        self.assertEquals(self.response.status_code, HTTP_200_OK)

    def test_render_with_all_needed_and_correct_templates(self):
        self.assertTemplateUsed(self.response, 'collaboratori/lista_collaboratori.html')
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'includes/menu.html')

    def test_page_contain_correct_table_head(self):
        table_head = "<thead><tr><th>Cognome</th><th>Nome</th><th>Dettagli</th></tr></thead>"
        self.assertInHTML(table_head, self.response.content.decode('utf8'))

    def test_page_contain_known_collaborator_but_no_details_because_lack_permission(self):
        utf8_content = self.response.content.decode('utf8')
        self.assertInHTML('Pace', utf8_content)
        self.assertInHTML('Gaspare', utf8_content)
        self.assertInHTML('<i class="fa fa-id-card" aria-hidden="true"></i>', utf8_content)


class FormTestsForLoggedInUsersWithPermissionsForListAndDetails(MyAccountTestCase):
    fixtures = ['collaboratori.json']

    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.COLLABORATORI_LISTA_READ, SiwPermessi.COLLABORATORE_MOSTRA}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)

    def test_page_contain_known_collaborator_and_details_icon(self):
        utf8_content = self.response.content.decode('utf8')
        self.assertInHTML('Pace', utf8_content)
        self.assertInHTML('Gaspare', utf8_content)
        self.assertInHTML('<a href = "/collaboratori/anagrafica/dettaglio/mostra/1/">'
                          '<span class="fa fa-id-card" aria-hidden="true"></span ></a>', utf8_content)

    def test_page_not_contains_add_link_without_permission(self):
        self.assertNotContains(self.response, '/collaboratori/anagrafica/propone-inserimento-collaboratore/')

    def test_page_contains_add_link_when_allowed(self):
        self.myuser.profile.permessi = {SiwPermessi.COLLABORATORI_LISTA_READ, SiwPermessi.COLLABORATORE_INSERISCE}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)
        self.assertContains(self.response, '/collaboratori/anagrafica/propone-inserimento-collaboratore/')
