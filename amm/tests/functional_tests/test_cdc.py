# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from accounts.models import User, SiwPermessi
from functional_tests.base import FunctionalTest


class LoginTest(FunctionalTest):
    # Crea l'utente per le prove.
    fixtures = ['cdc.json']
    
    def setUp(self):
        super().setUp()
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.user.profile.permessi = {SiwPermessi.AMM_CDC_READ, SiwPermessi.MENU_AMM, SiwPermessi.MENU_AMM_CDC}
        self.user.save(force_update=True)
        # Login
        self.browser.get(self.live_server_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('john')
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('secret123')
        button = self.browser.find_element_by_id('button_login')
        button.send_keys(Keys.ENTER)
    
    def test_cdc_page(self):
        # Naviga nei menù per arrivare a quello dei Centri di Costo
        menu = self.browser.find_element_by_xpath("//*[starts-with(.,'Amministrazione')]")
        ActionChains(self.browser).move_to_element(menu).perform()
        self.browser.find_element_by_link_text('Centri di Costo').send_keys(Keys.ENTER)
        
        # Controlla che nella pagina che trova ci sia AF 2018-2019
        self.assertIn('AF 2018-2019', self.browser.page_source)
        
        # Espande completamente l'albero dei centri di costo.
        self.browser.find_element_by_id('jqxbutton').send_keys(Keys.ENTER)
        
        # Adesso seleziona quello di PF44
        menu_pf44 = self.browser.find_element_by_xpath(
            "//li[contains(@class, 'jqx-tree-item-li') and contains(.//div, 'PF44')]")
        ActionChains(self.browser).move_to_element_with_offset(menu_pf44, 10, 10).click().perform()
        
        # Gli da il tempo di popolare il frame e poi controllo se trovo il dettaglio del Centro di Costo.
        try:
            WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "dettaglio_cdc")))
        finally:
            pass
        dettaglio_cdc = self.browser.find_element_by_id("dettaglio_cdc")
        self.assertIn('Progetto Formativo PF44', dettaglio_cdc.text)
