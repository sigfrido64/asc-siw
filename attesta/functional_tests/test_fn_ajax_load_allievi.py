# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.urls import reverse
from accounts.models import User, SiwPermessi
from functional_tests.base import FunctionalTest


class AjaxLoadAllieviTest(FunctionalTest):
    # Crea l'utente per le prove.
    # La parte di SQL Server non va caricata perchè è esterna al mio DB.
    def setUp(self):
        # Chiamo subito il costruttore della classe madre così poi posso operare su tutte le variabili che crea.
        super().setUp()
        # Creo l'utente per le prove. Lo faccio di qui senza fixtures per evitare i problemi del profilo che è
        # legato con i segnali e diversamente non funziona.
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Dati dell'utente
        self.myuser = User.objects.get(username=self.username)
        # Link alla vista
        self.url = "%s%s?corso=AMUC31" % (self.live_server_url, reverse('attesta:ajax_load_allievi'))
        
    def test_guest_forbidden(self):
        # Utente non loggato -> Forbidden
        self.browser.get(self.url)
        self.assertIn('403 Forbidden', self.browser.page_source)
    
    def test_user_no_perms_forbidden(self):
        # Utente che si è loggato ma non ha i permessi -> Forbidden
        # Mi loggo senza assegnare permessi.
        self.siw_do_login()
        
        # Prova ad accedere al link dell'api Ajax e mi aspetto Forbidden !!
        self.browser.get(self.url)
        self.assertIn('403 Forbidden', self.browser.page_source)

    def test_user_with_perms_grant(self):
        # Utente che si è loggato ed ha i permessi -> Grant !
        # Assegno i permessi all'utente.
        self.myuser.profile.permessi = {SiwPermessi.STAMPE_MDL}
        self.myuser.save(force_update=True)
        # Mi loggo.
        self.siw_do_login()

        # A questo punto prova ad accedere al link dell'api Ajax e mi aspetto Forbidden !!
        self.browser.get(self.url)
        self.assertIn('Zulianello', self.browser.page_source)
