# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from accounts.models import SiwPermessi
from ..ajax import ajax_dettaglio_persona_view

# Url della vista scritto sia in modo diretto che in modo interno.
ID_PERSONA = 50722
URL = f"/anagrafe/ajax/dettaglio-persona/{ID_PERSONA}/"
REVERSE_URL = 'anagrafe:ajax_dettaglio_persona'


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL, kwargs={'pk_persona': ID_PERSONA})
        self.assertEquals(url, URL)

    def test_dettaglio_persona_url_resolves_dettaglio_persona_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, ajax_dettaglio_persona_view)


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


class PermissionRequiredTests(MyAccountTestCase):
    def test_deny_for_logged_in_user_not_authorized_on_app(self):
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)


class FormGeneralTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['collaboratori.json']

    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.ANAGRAFE_DETTAGLIO_PERSONA}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_server_serve_page_without_errors(self):
        self.response = self.client.get(URL)
        self.assertEquals(self.response.status_code, HTTP_200_OK)

    def test_use_correct_template(self):
        self.response = self.client.get(URL)
        self.assertTemplateUsed(self.response, 'anagrafe/dettaglio_persona.html')
        self.assertTemplateUsed(self.response, 'includes/form_systemdata.html')

    def test_template_for_already_inserted_collaborator(self):
        self.response = self.client.get(URL)
        self.assertContains(self.response, 'Via Leopardi')
        self.assertContains(self.response, 'BSSFLV58E15L219M')
