# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.urls import reverse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from accounts.models import User, SiwPermessi
from functional_tests.base import FunctionalTest, scrive_data, scrive_nota

import time


class LoginTest(FunctionalTest):
    fixtures = ['cdc', 'corsi', 'af']
    
    def setUp(self):
        # Crea l'utente per le prove.
        super().setUp()
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.user.profile.permessi = {SiwPermessi.CORSI_LISTA_READ, SiwPermessi.CORSI_MODIFICA,
                                      SiwPermessi.CORSI_MOSTRA, SiwPermessi.MENU_CORSI, SiwPermessi.MENU_CORSI_LISTA}
        self.user.save(force_update=True)
        # Login
        self.browser.get(self.live_server_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('john')
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('secret123')
        button = self.browser.find_element_by_id('button_login')
        button.send_keys(Keys.ENTER)
    
    def test_modifica_corso(self):
        # Navigo nei menù per arrivare a quello dei Centri di Costo
        menu = self.browser.find_element_by_xpath("//*[starts-with(.,'Corsi')]")
        ActionChains(self.browser).move_to_element(menu).perform()
        self.browser.find_element_by_link_text('Lista Corsi').send_keys(Keys.ENTER)
        
        # Controllo che ci sia la lista in quanto trovo almeno un corso noto.
        self.assertIn('CCEA438', self.browser.page_source)

        # Premo il link di dettaglio.
        url = reverse('corsi:dettaglio_corso', kwargs={'pk': 'CCEA438'})
        self.browser.find_element_by_xpath('//a[@href="' + url + '"]').click()

        # Poi quello di modifica.
        time.sleep(0.5)
        self.browser.find_element_by_id('modifica_corso_link').click()
        
        # Compilo i campi con i dati del nuovo corso
        time.sleep(0.5)
        self.browser.execute_script("document.getElementById('id_denominazione').value='Corso di Prova by SIG'")
        
        self.browser.find_element_by_id('id_durata').send_keys(Keys.DELETE)
        
        # Imposto il cdc corretto.
        ActionChains(self.browser).move_to_element(self.browser.find_element_by_id('choose_cdc')).click().perform()

        # Adesso seleziona quello di PF44
        menu_af = self.browser.find_element_by_xpath(
            "//li[contains(@class, 'jqx-tree-item-li') and contains(.//div, 'AF 2018-2019')]")
        ActionChains(self.browser).move_to_element_with_offset(menu_af, 10, 10).click().perform()
        time.sleep(0.5)
        menu_pf = self.browser.find_element_by_xpath(
            "//li[contains(@class, 'jqx-tree-item-li') and contains(.//div, 'Apprendisti 2018-2019')]")
        ActionChains(self.browser).move_to_element_with_offset(menu_pf, 10, 10).click().perform()
        time.sleep(0.5)
        menu_pf1 = self.browser.find_element_by_xpath(
            "//li[contains(@class, 'jqx-tree-item-li') and contains(.//div, 'PF44')]")
        ActionChains(self.browser).move_to_element_with_offset(menu_pf1, 10, 10).click().perform()
        # Confermo la selezione.
        ActionChains(self.browser).move_to_element(self.browser.find_element_by_id('do_select')).click().perform()

        # Setto lo stato del corso usando il suo valore e non l'etichetta.
        self.browser.execute_script("$('#id_stato_corso').val('50')")
        
        # Date di inizio e di fine corso.
        scrive_data(self.browser, 'id_data_inizio', '13111964')
        scrive_data(self.browser, 'id_data_fine', '13111965')
        
        # Note
        scrive_nota(self.browser, 'id_note', 'Ciao')

        # Faccio l'insert
        self.browser.find_element_by_id('do_insert').click()
        
        # Aspetto di essere reindirizzato alla pagina della lista dei corsi.
        try:
            WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "tabella_lista_corsi")))
        finally:
            pass
        
        # Qui devo trovare il nuovo corso appena inserito.
        lista_corsi = self.browser.find_element_by_id("tabella_lista_corsi")
        self.assertIn('Corso di Prova by SIG', lista_corsi.text)
