# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from accounts.models import SiwPermessi
from ..ajax import ajax_elimina_ripartizione_su_cdc
from ..models import RipartizioneSpesaPerCDC, AcquistoConOrdine


# Url della vista scritto sia in modo diretto che in modo interno.
ID_PRESENTE = 1
URL = f"/acquisti/ajax/elimina_ripartizione_su_cdc/{ID_PRESENTE}/"
REVERSE_URL = reverse('acquisti:ajax_elimina_ripartizione_su_cdc', kwargs={'pk': ID_PRESENTE})


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        self.assertEquals(URL, REVERSE_URL)

    def test_delete_ripartizione_cdc_url_resolves_delete_ripartizione_cdc_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, ajax_elimina_ripartizione_su_cdc)


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi.
    Metto 'username' e 'passoword' e l'url della pagina che voglio testare come reverse
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


class LoginRequiredTests(MyAccountTestCase):
    def test_forbidden_for_not_logged_in_user(self):
        self.response = self.client.get(URL, {'cdcId': 1})
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)


class PermissionRequiredTests(MyAccountTestCase):
    def test_deny_for_logged_in_user_not_authorized_on_app(self):
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL, {'cdcId': 1})
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)


class FormGeneralTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['af', 'cdc', 'azienda', 'fornitore', 'ordine_acquisto', 'ripartizioni']

    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.ACQUISTI_CDC_ERASE}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_server_serve_page_without_errors(self):
        self.response = self.client.get(URL)
        self.assertEquals(self.response.status_code, HTTP_200_OK)

    def test_elimina_ripartizione_su_cdc(self):
        # Prima di eliminare le ripartizioni devono essere due.
        numero_ripartizioni = RipartizioneSpesaPerCDC.objects.filter(acquisto=1).count()
        self.assertEqual(numero_ripartizioni, 2)
        # E l'acquisto non deve essere dirty.
        acquisto = AcquistoConOrdine.objects.get(id=1)
        self.assertEqual(acquisto.dirty, False)
        
        # Elimino una ripartizione
        self.response = self.client.get(URL)
        # Verifico che risponda con ok.
        self.assertJSONEqual(self.response.content, {'risultato': 'ok'})
        
        # Dopo la cancellazione della prima ne dovrebbe restare esattamente solo una.
        numero_ripartizioni = RipartizioneSpesaPerCDC.objects.filter(acquisto=1).count()
        self.assertEqual(numero_ripartizioni, 1)
        # Controllo che l'acquisto adesso sia dirty e che non ci sia più un cdc_txt
        acquisto = AcquistoConOrdine.objects.get(id=1)
        self.assertEqual(acquisto.dirty, True)
