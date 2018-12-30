# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import SiwPermessi
from ..ajax import ajax_load_allievi


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi
    """
    fixtures = ['af']
    
    def setUp(self):
        # Fake user
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Dati dell'utente
        self.myuser = User.objects.get(username=self.username)
        # Link alla vista
        self.url = "%s?corso=AMUC31" % reverse('attesta:ajax_load_allievi')


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
