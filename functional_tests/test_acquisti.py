# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
import os
import poplib
import re
import time
from django.core import mail
from selenium.webdriver.common.keys import Keys

from accounts.models import User
from .base import FunctionalTest

URL_ACQUISTI = '/acquisti/'


class AcquistiTest(FunctionalTest):
    fixtures = ['auth.json', 'utenti.json']

    # TODO Da controllare perchè con il modello che lancia segnali non funzionava. Se tolgo i segnali funziona ma
    # bisogna capire che succede nella gestione dei permessi !
    ## Mi loggo ed accedo al menù degli acquisti.
    
    """
    # Crea l'utente per le prove.
    def setUp(self):
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.myuser = User.objects.get(username=self.username)
        super().setUp()
    """

    def Atest_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

    def test_log_in(self):
        # Mi collego alla pagina degli acquisti e siccome non sono loggato mi rimanda alla pagina di login.
        # Interessante per prendere il link al login !!!
        # self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        acquisti = f'{self.live_server_url}{URL_ACQUISTI}'
        response = self.browser.get(acquisti)
        self.fail("QUi non trovo la pagina ma devo vedere come gestire l'eccezzione !")
        
        time.sleep(5)
        
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('john')
        
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('secret123')
        
        button = self.browser.find_element_by_id('button_login')
        button.send_keys(Keys.ENTER)
        
        self.fail("Attenzione a rivedere il modello Utente !")
