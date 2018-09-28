# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from accounts.models import User, SiwPermessi
from functional_tests.base import FunctionalTest

import time

SUBJECT = 'Your login link for Superlists'


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
        action = ActionChains(self.browser)
        menu = self.browser.find_element_by_xpath("//*[starts-with(.,'Amministrazione')]")
        action.move_to_element(menu)
        action.perform()
        menu_item = self.browser.find_element_by_link_text('Centri di Costo')
        menu_item.send_keys(Keys.ENTER)
        
        # Controlla che nella pagina che trova ci sia AF 2018-2019
        self.assertIn('AF 2018-2019', self.browser.page_source)
        
        # Espande completamente l'albero dei centri di costo.
        expand = self.browser.find_element_by_id('jqxbutton')
        expand.send_keys(Keys.ENTER)
        
        # Adesso seleziona quello di PF44
        pf44 = ActionChains(self.browser)
        menu_pf44 = self.browser.find_element_by_xpath("//li[contains(@class, 'jqx-tree-item-li') and contains(.//div, 'PF44')]")
        pf44.move_to_element_with_offset(menu_pf44, 10, 10)
        pf44.click()
        pf44.perform()
        # ActionChains(self.browser).move_to_element(menu_pf44).perform()
        # Gli da il tempo di popolare il frame
        # TODO E' giusto fare così ?
        time.sleep(1)

        # Controlla che nella pagina che trova ci sia AF 2018-2019
        self.assertIn('Progetto Formativo PF44', self.browser.page_source)

"""
SPUNTO INTERESSANTE

WebElement admin = driver.findElement(By.xpath("//b[contains(., 'Admin')]"));

new Actions(driver).moveToElement(admin).perform();

WebElement userManagement = new WebDriverWait(driver, 5).until(ExpectedConditions.elementToBeClickable(By.id("menu_admin_UserManagement")));
new Actions(driver).moveToElement(userManagement).perform();

WebElement users = new WebDriverWait(driver, 5).until(ExpectedConditions.elementToBeClickable(By.id("menu_admin_viewSystemUsers")));
users.click();
"""
