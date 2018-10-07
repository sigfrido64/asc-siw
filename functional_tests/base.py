import os
from datetime import datetime
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
import time

# from .server_tools import reset_database
# from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

MAX_WAIT = 10

CHROME = True


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


def scrive_data(web_broser_instance, id_field, date_as_raw_string):
    wbi = web_broser_instance
    ActionChains(wbi).move_to_element(wbi.find_element_by_id(id_field)).click().pause(0.5).\
        send_keys(Keys.ARROW_LEFT).send_keys(Keys.ARROW_LEFT).send_keys(date_as_raw_string).perform()


def scrive_nota(web_broser_instance, id_field, testo_per_nota):
    wbi = web_broser_instance
    ActionChains(wbi).move_to_element(wbi.find_element_by_id(id_field)).click().pause(0.5).\
        send_keys(testo_per_nota).perform()


class FunctionalTest(StaticLiveServerTestCase):
    
    @staticmethod
    def __check_error(message):
        # Se è un forbidden lo gestisco più ad alto livello.
        if '403 (Forbidden)' in message:
            return False
        # Gli errori di favicon non li guardo perchè per Ajax non è previsto.
        if 'favicon.ico - Failed to load resource:':
            return False
        return True

    def setUp(self):
        # To be overriden
        self.username = self.password = None
        
        # Avvio il driver corrispondente al tipo di Browser che voglio usare.
        if CHROME:
            d = DesiredCapabilities.CHROME
            d['loggingPrefs'] = {'browser': 'SEVERE'}
            self.browser = webdriver.Chrome(desired_capabilities=d)
        else:
            self.browser = webdriver.Firefox()
            
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            print("Stagin server !")
            self.live_server_url = 'http://' + self.staging_server
            # reset_database(self.staging_server)
        self.browser.implicitly_wait(5)  # Max 10 Sec di attesa prima di un find_element

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
                
        # Se uso Chrome posso accedere anche agli errori del Browser
        if CHROME:
            # Se ci sono errori (log level SEVERE) li stampo e segnalo il fail !
            errori = self.browser.get_log('browser')
            if errori:
                trovati = False
                for entry in errori:
                    if self.__check_error(entry['message']):
                        print("ERRORE : ", entry['message'])
                        trovati = True
                if trovati:
                    self.fail("Errori segnalati dal Browser !!! Leggi sopra !!!")
                
        # Chiudo il Browser.
        if CHROME:
            self.browser.close()
        self.browser.quit()
        
        # Qui inutile perchè nella definizione della classe ha solo 'pass'
        super().tearDown()

    def _test_has_failed(self):
        # slightly obscure but couldn't find a better way!
        return any(error for (method, error) in self._outcome.errors)


    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)


    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)


    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )


    @wait
    def wait_for(self, fn):
        return fn()


    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        """
        Recupera dal Browser un elemento in base al suo nome.
        :return:
        """
        return self.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
        
    def siw_do_login(self):
        # Esegue il login con le credenziali fornite.
        # Parto dalla pagina di login
        url = "%s/login/" % self.live_server_url
        self.browser.get(url)
    
        # Inserisce nome utente e password.
        self.browser.find_element_by_name('username').send_keys(self.username)
        self.browser.find_element_by_name('password').send_keys(self.password)
        # Clicca su login
        self.browser.find_element_by_id('button_login').send_keys(Keys.ENTER)
    
        # Controlla che il login sia andato a buon fine.
        self.browser.find_element_by_id('id_logout')

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))
