# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from accounts.models import User, SiwPermessi
from functional_tests.base import FunctionalTest

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
        action = ActionChains(self.browser)
        menu = self.browser.find_element_by_xpath('//*[@id="menuItem9904713779915311000"]')
        hidden_submenu = self.browser.find_element_by_xpath('//*[@id="menuItem99009463157353090000"]/a')

        action.move_to_element(menu)
        action.click(hidden_submenu)
        action.perform()

        self.fail('Va a finire il test')
