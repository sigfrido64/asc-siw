# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from accounts.models import SiwPermessi
from ..ajax import ajax_lista_ripartizioni_per_ordine_web


# Url della vista scritto sia in modo diretto che in modo interno.
ID_ORDINE = 1
URL = f"/acquisti/ajax/lista_ripartizioni_per_ordine_web/{ID_ORDINE}/"
REVERSE_URL = reverse('acquisti:ajax_lista_ripartizioni_per_ordine_web', kwargs={'pk': ID_ORDINE})


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        self.assertEquals(URL, REVERSE_URL)

    def test_lista_ripartizioni_url_resolves_lista_ripartizioni_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, ajax_lista_ripartizioni_per_ordine_web)


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi.
    Metto 'username' e 'password' e l'url della pagina che voglio testare come reverse
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
    def test_forbidden_for_not_logged_in_user(self):
        self.response = self.client.get(URL, {'cdcId': 1})
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)


class PermissionRequiredTests(MyAccountTestCase):
    def test_deny_for_logged_in_user_not_authorized_on_app(self):
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL, {'cdcId': 1})
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)


class FormGeneralTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['af', 'cdc', 'acquisto_web', 'ripartizioni_web']

    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.ACQUISTI_ORDINI_VIEW}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_verifica_ripartizioni_delle_fixturs(self):
        self.response = self.client.get(URL)
        self.assertEquals(self.response.status_code, HTTP_200_OK)
        self.assertContains(self.response, 'FIMA Conto Sistema 2018-2019')

