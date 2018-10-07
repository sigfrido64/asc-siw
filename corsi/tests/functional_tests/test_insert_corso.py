# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from accounts.models import User, SiwPermessi
from functional_tests.base import FunctionalTest

import time


def scrive_data(web_broser_instance, id_field, date_as_raw_string):
    wbi = web_broser_instance
    ActionChains(wbi).move_to_element(wbi.find_element_by_id(id_field)).click().pause(0.5).\
        send_keys(Keys.ARROW_LEFT).send_keys(Keys.ARROW_LEFT).send_keys(date_as_raw_string).perform()


def scrive_nota(web_broser_instance, id_field, testo_per_nota):
    wbi = web_broser_instance
    ActionChains(wbi).move_to_element(wbi.find_element_by_id(id_field)).click().pause(0.5).\
        send_keys(testo_per_nota).perform()


class LoginTest(FunctionalTest):
    fixtures = ['cdc.json', 'corsi.json']
    
    def setUp(self):
        # Crea l'utente per le prove.
        super().setUp()
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.user.profile.permessi = {SiwPermessi.CORSI_LISTA_READ, SiwPermessi.CORSI_INSERISCE,
                                      SiwPermessi.MENU_CORSI, SiwPermessi.MENU_CORSI_LISTA}
        self.user.save(force_update=True)
        # Login
        self.browser.get(self.live_server_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('john')
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('secret123')
        button = self.browser.find_element_by_id('button_login')
        button.send_keys(Keys.ENTER)
    
    def test_inserisce_corso(self):
        # Navigo nei menù per arrivare a quello dei Centri di Costo
        menu = self.browser.find_element_by_xpath("//*[starts-with(.,'Corsi')]")
        ActionChains(self.browser).move_to_element(menu).perform()
        self.browser.find_element_by_link_text('Lista Corsi').send_keys(Keys.ENTER)
        
        # Controllo che ci sia la lista in quanto trovo almeno un corso noto.
        self.assertIn('CCEA438', self.browser.page_source)

        # Premo il tasto di inserimento.
        self.browser.find_element_by_id('inserisce_corso').send_keys(Keys.ENTER)

        # Compilo i campi con i dati del nuovo corso
        self.browser.find_element_by_id('id_codice_edizione').send_keys('SIGI123')
        self.browser.find_element_by_id('id_denominazione').send_keys('Corso di Prova by SIG')
        self.browser.find_element_by_id('id_durata').send_keys('60')
        
        # Imposto il cdc corretto.
        ActionChains(self.browser).move_to_element(self.browser.find_element_by_id('choose_cdc')).click().perform()
        time.sleep(5)
        
        # Setto lo stato del corso.
        ActionChains(self.browser).move_to_element(self.browser.find_element_by_id('id_stato_corso')).\
            click().send_keys(Keys.ARROW_DOWN).perform()
        # Date di inizio e di fine corso.
        scrive_data(self.browser, 'id_data_inizio', '13111964')
        scrive_data(self.browser, 'id_data_fine', '13111965')
        
        # Note
        ActionChains(self.browser).move_to_element(self.browser.find_element_by_id('id_note')).\
            click().pause(0.5).send_keys('Ciao').perform()

        # Faccio l'insert
        self.browser.find_element_by_id('do_insert').click()
        
        time.sleep(5)
        self.fail('Va a finire il test !')
        