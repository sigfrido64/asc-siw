# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from unittest import skip
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from accounts.models import SiwPermessi
from ..ajax import ajax_load_tutte_persone


# Url della vista scritto sia in modo diretto che in modo interno.
URL = f"/collaboratori/ajax/load-persone/"
REVERSE_URL = 'collaboratori:ajax_load_tutte_persone'


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL)
        self.assertEquals(url, URL)

    def test_inserisce_collaboratore_url_resolves_inserisce_collaboratore_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, ajax_load_tutte_persone)


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

@skip
class NoPermsForbiddenTests(MyAccountTestCase):
    def test_guest_forbidden(self):
        # Utente non loggato -> Forbidden
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 403)
        
    def test_no_perms_on_app(self):
        # Utente che si è loggato ma non ha i permessi -> Forbidden
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 403)


@skip
class AjaxGeneralTests(MyAccountTestCase):
    def setUp(self):
        # Utente che si logga con permessi. Faccio gli altri test
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        # Il server riesce a fornire la pagina richiesta.
        self.assertEquals(self.response.status_code, 200)
        
    def test_url_resolves_correct_view(self):
        # La risoluzione dell'url mi manda alla funzione corretta
        ajax = resolve('/attesta/ajax/load-allievi/')
        self.assertEquals(ajax.func, ajax_load_allievi)
    
    def test_use_template(self):
        # Controllo che usi il template corretto.
        self.assertTemplateUsed(self.response, 'attesta/allievi_list_table.html',
                                "Non è stato usato il template corretto")
        
    def test_response(self):
        # Nella risposta devo avere la lista dei corsi. Ne controllo un paio..
        self.assertContains(self.response, '<td>Cardone</td>')
