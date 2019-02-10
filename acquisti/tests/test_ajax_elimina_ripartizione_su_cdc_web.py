# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from accounts.models import SiwPermessi
from ..ajax import ajax_elimina_ripartizione_su_cdc_web
from ..models import RipartizioneAcquistoWebPerCDC, AcquistoWeb

# Url della vista scritto sia in modo diretto che in modo interno.
ID_PRESENTE = 1
URL = f"/acquisti/ajax/elimina_ripartizione_su_cdc_web/"
REVERSE_URL = 'acquisti:ajax_elimina_ripartizione_su_cdc_web'


class GeneralTests(TestCase):
    def setUp(self):
        chiave = 1
        self.url = URL + str(chiave) + '/'
        self.reverse_url = reverse(REVERSE_URL, kwargs={'pk': chiave})

    def test_url_and_reverseurl_equality(self):
        self.assertEquals(self.url, self.reverse_url)

    def test_delete_ripartizione_cdc_web_url_resolves_delete_ripartizione_cdc_web_view(self):
        view = resolve(self.url)
        self.assertEquals(view.func, ajax_elimina_ripartizione_su_cdc_web)


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi.
    Metto 'username' e 'password' e l'url della pagina che voglio testare come reverse
    """
    fixtures = ['af']
    
    def setUp(self):
        # Fake user
        self.fake_user_username = 'john'
        self.fake_user_password = 'secret123'
        self.user = User.objects.create_user(username=self.fake_user_username, email='john@doe.com',
                                             password=self.fake_user_password)
        # Recupero tutti i Dati dell'utente, serve dopo per aggiungere i permessi.
        self.myuser = User.objects.get(username=self.fake_user_username)
        # Mi creo un link valido per le prove. Uso la ripartizione di pk=1.
        # Anche se qui non carico le fixtures, per cui non la trovo, va bene in quanto i primi test sono solo per
        # le prove sui link e sulla loro raggiungibilità.
        self.url = URL + str(ID_PRESENTE) + '/'
        

class LoginRequiredTests(MyAccountTestCase):
    def test_forbidden_for_not_logged_in_user(self):
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)


class PermissionRequiredTests(MyAccountTestCase):
    def test_deny_for_logged_in_user_not_authorized_on_app(self):
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)


class FormGeneralTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['af', 'cdc', 'acquisto_web', 'ripartizioni_web']

    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.ACQUISTI_CDC_ERASE}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_server_serve_page_without_errors(self):
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, HTTP_200_OK)

    def test_elimina_ripartizione_su_cdc(self):
        # Prima di eliminare le ripartizioni controllo che siano due.
        numero_ripartizioni = RipartizioneAcquistoWebPerCDC.objects.filter(acquisto_web=ID_PRESENTE).count()
        self.assertEqual(numero_ripartizioni, 2)
        # E l'acquisto non deve essere dirty.
        acquisto = AcquistoWeb.objects.get(id=1)
        self.assertEqual(acquisto.dirty, False)
        
        # Elimino una ripartizione
        self.response = self.client.get(self.url)
        # Verifico che risponda con ok.
        self.assertJSONEqual(self.response.content, {'risultato': 'ok'})
        
        # Dopo la cancellazione della prima ne dovrebbe restare esattamente solo una.
        numero_ripartizioni = RipartizioneAcquistoWebPerCDC.objects.filter(acquisto_web=ID_PRESENTE).count()
        self.assertEqual(numero_ripartizioni, 1)
        
        # L'acquisto adesso deve essere dirty
        acquisto = AcquistoWeb.objects.get(id=1)
        self.assertEqual(acquisto.dirty, True)
        
        # Il cdc_verbose deve essere None in quanto incompleto.
        self.assertEqual(acquisto.cdc_verbose, None)
