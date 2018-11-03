# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from accounts.models import User, SiwPermessi
from functional_tests.base import FunctionalTest

"""
TODO
Bisogna creare anche tutti gli altri test funzionali per inserimento e modifica di un elemento.
"""


class LoginTest(FunctionalTest):
    # Crea l'utente per le prove.
    fixtures = ['collaboratori.json']
    
    def setUp(self):
        super().setUp()
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.user.profile.permessi = {SiwPermessi.COLLABORATORE_MOSTRA, SiwPermessi.COLLABORATORI_LISTA_READ,
                                      SiwPermessi.MENU_COLLABORATORI, SiwPermessi.MENU_COLLABORATORI_LISTA,
                                      SiwPermessi.ANAGRAFE_DETTAGLIO_PERSONA_MOSTRA}
        self.user.save(force_update=True)
        # Login
        self.browser.get(self.live_server_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('john')
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('secret123')
        button = self.browser.find_element_by_id('button_login')
        button.send_keys(Keys.ENTER)
    
    def test_vista_mostra_dettaglio_collaboratore(self):
        # Naviga nei menù per arrivare a quello dei Centri di Costo
        menu = self.browser.find_element_by_xpath("//*[starts-with(.,'Collaboratori')]")
        ActionChains(self.browser).move_to_element(menu).perform()
        self.browser.find_element_by_link_text('Lista Collaboratori').send_keys(Keys.ENTER)
        
        # Controllo che ci sia un collaboratore noto tra quelli che ho nelle fixtures.
        cella = self.browser.find_element_by_xpath("//table/tbody/tr[1]/td[1]")
        self.assertIn('Pace', cella.text)
        cella = self.browser.find_element_by_xpath("//table/tbody/tr[1]/td[2]")
        self.assertIn('Gaspare', cella.text)
        
        # Ora apro la maschera del dettaglio del collaboratore.
        cella = self.browser.find_element_by_xpath("//table/tbody/tr[1]/td[3]")
        cella.find_element_by_tag_name('a').click()
        
        # Aspetta di essere rediretto alla nuova pagina.
        try:
            WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "dettaglio_collaboratore")))
        finally:
            pass
        
        # Chiede il dettaglio dell'anagrafica del collaboratore.
        self.browser.find_element_by_id("dettaglio_collaboratore").click()
        
        # Aspetta che si popoli la finestra con i contenuti.
        try:
            WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "dettaglio_anagrafica_persona")))
        finally:
            pass
        
        # Controllo che ci siano i dettagli dell'anagrafica del collaboratore.
        cella = self.browser.find_element_by_id("dettaglio_anagrafica_persona")
        self.assertIn('Piscina', cella.text)
        self.assertIn('Tunisia', cella.text)
