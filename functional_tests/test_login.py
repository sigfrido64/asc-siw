# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from selenium.webdriver.common.keys import Keys
from accounts.models import User
from .base import FunctionalTest


SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    # fixtures = ['auth.json', 'utenti.json']
    # TODO Da controllare perchè con il modello che lancia segnali non funzionava. Se tolgo i segnali funziona ma
    # bisogna capire che succede nella gestione dei permessi !
    
    # Crea l'utente per le prove.
    def setUp(self):
        # Chiamo subito il costruttore della classe madre così poi posso operare su tutte le variabili
        # che crea.
        super().setUp()
        # Creo l'utente per le prove. Lo faccio di qui senza fixtures per evitare i problemi del profilo che è
        # legato con i segnali e diversamente non funziona.
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)

    def test_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        if self.staging_server:
            test_email = 'edith.testuser@yahoo.com'
        else:
            test_email = 'edith@example.com'
        
        # Interessante per prendere il link al login !!!
        # self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        self.browser.get(self.live_server_url)
        # for entry in self.browser.get_log('browser'):
        #     print(entry)
        
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('john')
        
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('secret123')
        
        button = self.browser.find_element_by_id('button_login')
        button.send_keys(Keys.ENTER)
        
        self.fail("Vai a finire i test")
