# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import SiwPermessi
from unittest import skip
from ..ajax import ajax_load_reports
__author__ = "Pilone Ing. Sigfrido"


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
        self.url = "%s?corso=PLCC19" % reverse('attesta:ajax_load_reports')


class LoginRequiredTests(MyAccountTestCase):
    # Test per utente non loggato o guest.
    def test_guest_forbidden(self):
        # Un utente non loggato non deve avere accesso.
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 403)


class NoPermsTests(MyAccountTestCase):
    # Utente regolare e loggato ma senza privilegi.
    def test_no_perms_on_app(self):
        # Un utente regolarmente loggato ma senza privilegi non deve avere accesso.
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 403)


class AjaxGeneralTests(MyAccountTestCase):
    # Utente loggato e con permessi.
    # Carico il database di esempio per i report
    fixtures = ['reports', 'af']

    def setUp(self):
        # Inizializzazioni generali per utente che si logga con permessi.
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
        ajax = resolve('/attesta/ajax/load-reports/')
        self.assertEquals(ajax.func, ajax_load_reports)

    def test_use_template(self):
        # Controllo che usi il template corretto.
        self.assertTemplateUsed(self.response, 'attesta/reports_list_options.html',
                                "Non è stato usato il template corretto")

    def test_response(self):
        # Nella risposta devo avere la lista dei corsi. Controllo le due voci che dovrei trovare
        self.assertContains(self.response, '<option value="iscrizione_mdl">')
        self.assertContains(self.response, '<option value="frequenza_mdl_t1">')
        self.assertContains(self.response, '<option value="frequenza_mdl_gg">')
