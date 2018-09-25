# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from unittest import skip
from django.urls import reverse, resolve
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from accounts.models import SiwPermessi
from ..ajax import ajax_centri_di_costo_per_treeview


# Url della vista scritto sia in modo diretto che in modo interno.
URL = f"/amm/ajax/list-cdc/"
REVERSE_URL = 'amm:ajax_centri_di_costo_per_treeview'


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL)
        self.assertEquals(url, URL)

    def test_list_cdc_url_resolves_ajax_centri_di_costo_per_treeview(self):
        view = resolve(URL)
        self.assertEquals(view.func, ajax_centri_di_costo_per_treeview)


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
    def test_forbidden_for_not_logged_in_user(self):
        self.response = self.client.get(URL)
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)

@skip
class PermissionRequiredTests(MyAccountTestCase):
    def test_deny_for_logged_in_user_not_authorized_on_app(self):
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL, {'name_starts_with': 'pac'})
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
        self.response = self.client.get(URL, {'name_starts_with': 'pac'})

    def test_server_serve_page_without_errors(self):
        self.assertEquals(self.response.status_code, HTTP_200_OK)

    def test_lista_persone_note(self):
        self.assertContains(self.response, 'Pace')
        self.assertContains(self.response, 'Gaspare')
