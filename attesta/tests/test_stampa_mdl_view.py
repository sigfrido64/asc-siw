# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.conf import settings
from accounts.models import SiwPermessi
from ..views import stampa_mdl
from unipath import Path
__author__ = "Pilone Ing. Sigfrido"


URL = '/attesta/stampe/mdl/iscrizione_mdl/PLCC19/926/12-03-2018/'  # Questo è il link che ho scritto nelle urls per arrivare a questa vista.
REVERSE_URL = 'attesta:stampa_mdl'  # Questa è la stringa che uso per il reverse per vedere che link genera.
# reverse('admin:app_list', kwargs={'app_label': 'auth'})
#  path('stampe/mdl/<str:report>/<str:corso>/<int:matricola>/<str:data_stampa>', views.stampa_mdl, name='stampa_mdl'),


class MyAccountTestCase(TestCase):
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
        # Link alla vista
        self.url = reverse(REVERSE_URL, kwargs={'reportname': 'iscrizione_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                                'data_stampa': '12-03-2018'})
        
        
class LoginRequiredTests(TestCase):
    # Test che faccio per un utente non loggato, un utente guest.
    # Quindi eredito da TestCase e non da MyAccount in quanto non ho informazioni di Login.
    def test_redirection(self):
        # Un utente non loggato deve essere rediretto alla pagina di login.
        self.url = reverse(REVERSE_URL, kwargs={'reportname': 'iscrizione_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                                'data_stampa': '12-03-2018'})
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class PermissionRequiredTests(TestCase):
    # Qui metto i test per un utente che si logga ma che non ha i permessi per accedere all'app.
    # Anche qui eredito da TestCase e non da MyAccount in quanto testo solo il login e non i permessi.
    def setUp(self):
        # Fake user & login
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Dati dell'utente
        self.myuser = User.objects.get(username=self.username)
        # Eseguo il login
        self.client.login(username=self.username, password=self.password)
        # Link alla vista
        self.url = reverse(REVERSE_URL, kwargs={'reportname': 'iscrizione_mdl', 'corso': 'PLCC19', 'matricola': 926,
                                                'data_stampa': '12-03-2018'})
    
    def test_no_perms_on_app(self):
        # Un utente che si logga senza permessi e prova ad accere alla pagina dell'applicazione deve ricevere
        # come risposta 403 = Denied !
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 403)
        
    def test_url_resolves_correct_view(self):
        # Se invece ho i permessi la risoluzione dell'url mi manda alla vista corretta.
        # Il test fallisce quando il link non mi porta alla vista e devi guardare negli urls dell'app.
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        view = resolve(self.url)
        self.assertEquals(view.func, stampa_mdl)
