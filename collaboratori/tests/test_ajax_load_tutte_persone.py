# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from unittest import skip
from accounts.models import SiwPermessi


# Url della vista scritto sia in modo diretto che in modo interno.
URL = f"/collaboratori/anagrafica/inserisce-nuovo/"
REVERSE_URL = 'collaboratori:inserisce_nuovo'

@skip
class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL)
        self.assertEquals(url, URL)

    def test_inserisce_collaboratore_url_resolves_inserisce_collaboratore_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, propone_inserimento_collaboratore_view)


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi
    """
    def setUp(self):
        # Fake user
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Dati dell'utente
        self.myuser = User.objects.get(username=self.username)
        # Link alla vista
        self.url = "%s?corso=AMUC31" % reverse('attesta:ajax_load_allievi')


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
