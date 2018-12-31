# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from accounts.models import SiwPermessi


URL = '/'  # Link alla home dell'applicazione, qui devo vedere un menù se sono autorizzato.
REVERSE_URL = 'home'  # Reverse della home page !
MENU_ITEM_LINK = '/acquisti/'     # Il link che voglio trovare per capire che quel menù è presente.


class MyAccountTestCase(TestCase):
    fixtures = ['af']
    """
    Qui metto le informazioni di base per i test successivi.
    Metto 'username' e 'passoword' e l'url della pagina che voglio testare come reverse
    """
    def setUp(self):
        # Fake user
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Dati dell'utente
        self.myuser = User.objects.get(username=self.username)
        self.url = reverse(REVERSE_URL)


class LoginRequiredTests(MyAccountTestCase):
    """
    Test che faccio per utenti non loggati.
    """
    def test_match(self):
        # Prima di tutto controllo se il link diretto e quello che ottengo con il resolve coincidono.
        self.assertEquals(URL, self.url)

    def test_redirection(self):
        # Un utente non loggato deve essere rediretto alla pagina di login.
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class PermissionRequiredTests(MyAccountTestCase):
    def test_no_menu_on_home(self):
        # Un utente che si logga senza permessi ed accede alla home non deve trovare la voce di menù !
        # Attezione che nel template che genera il menù non ho il riferimento alla classe ! (che vuol dire?)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        self.assertNotContains(self.response, MENU_ITEM_LINK)


class FormGeneralTests(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.MENU_AMM, SiwPermessi.MENU_AMM_ACQUISTI}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_menu_sotto_amministrazione_menu(self):
        # Quando accedo alla home devo trovare la voce di menù per la mia app.
        # Il test fallisce quando nel menù generale non trovo il link a questa vista.
        # Il link viene messo nel template menu.html che trovi in templates/includes
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        self.assertContains(self.response, MENU_ITEM_LINK)
