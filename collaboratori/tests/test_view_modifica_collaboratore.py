# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import SiwPermessi
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from ..views import modifica_collaboratore_view

from unittest import skip

# TODO Bisogna creare i test per la parte di modifica vera e propria mettendo i valori nei campi e verificando che
# vada a buon fine.

# Url della vista scritto sia in modo diretto che in modo interno.
ID_PRESENTE = 1
ID_ASSENTE = 13
URL_PRESENTE = f"/collaboratori/anagrafica/modifica/{ID_PRESENTE}/"
URL_ASSENTE = f"/collaboratori/anagrafica/modifica/{ID_ASSENTE}/"
REVERSE_URL = 'collaboratori:modifica_esistente'


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL, kwargs={'pk_collaboratore': ID_PRESENTE})
        self.assertEquals(url, URL_PRESENTE)

    def test_modifica_collaboratore_url_resolves_modifica_collaboratore_view(self):
        view = resolve(URL_PRESENTE)
        self.assertEquals(view.func, modifica_collaboratore_view)

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

@skip
class LoginRequiredTests(MyAccountTestCase):
    def test_redirection_to_login_for_not_logged_in_user(self):
        login_url = reverse('login')
        response = self.client.get(URL_PRESENTE)
        self.assertRedirects(response, f'{login_url}?next={URL_PRESENTE}')

@skip
class PermissionRequiredTests(MyAccountTestCase):
    def test_deny_for_logged_in_user_not_authorized_on_app(self):
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL_PRESENTE)
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)

@skip
class FormGeneralTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['collaboratori.json']

    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.COLLABORATORE_INSERISCE}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_server_serve_page_without_errors(self):
        self.response = self.client.get(URL_PRESENTE)
        self.assertEquals(self.response.status_code, HTTP_200_OK)

    def test_render_error_collaborator_already_present_with_error_templates(self):
        self.response = self.client.get(URL_PRESENTE)
        self.assertTemplateUsed(self.response, 'collaboratori/errore_collaboratore_gia_presente.html')
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'includes/menu.html')

    def test_render_new_collaborator_with_correct_templates(self):
        self.response = self.client.get(URL_NUOVO)
        self.assertTemplateUsed(self.response, 'collaboratori/inserisce_collaboratore.html')
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'includes/menu.html')
