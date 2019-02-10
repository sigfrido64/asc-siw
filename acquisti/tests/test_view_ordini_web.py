# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import SiwPermessi
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from ..views import ordini_web

from unittest import skip

# Url della vista scritto sia in modo diretto che in modo interno.
URL = f"/acquisti/ordini_web/"
REVERSE_URL = 'acquisti:ordini_web'


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL)
        self.assertEquals(url, URL)

    def test_ordini_url_resolves_ordini_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, ordini_web)


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
    fixtures = ['af']
    
    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.ACQUISTI_ORDINI_VIEW}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_server_serve_page_without_errors(self):
        self.response = self.client.get(URL)
        self.assertEquals(self.response.status_code, HTTP_200_OK)
        
    def test_render_with_correct_templates(self):
        self.response = self.client.get(URL)
        self.assertTemplateUsed(self.response, 'acquisti/ordini_web.html')

    def test_correct_title(self):
        self.response = self.client.get(URL)
        self.assertContains(self.response, 'Lista Ordini Web')

    def test_find_insert_button_when_allowed(self):
        self.myuser.profile.permessi = {SiwPermessi.ACQUISTI_ORDINI_VIEW, SiwPermessi.ACQUISTI_ORDINI_INSERISCE}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)
        url = reverse('acquisti:ordine_inserisce')
        self.assertContains(self.response, url)

    def test_find_link_to_insert_when_allowed(self):
        self.fail("Vai a finire il test per questo caso e per quello opposto.")
