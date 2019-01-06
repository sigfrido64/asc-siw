# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import SiwPermessi
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_302_FOUND
from ..views import inserimento_cdc
from ..forms import RipartizioneForm
from ..models import AcquistoConOrdine, RipartizioneSpesaPerCDC
from siw.sig_utils import response_debug

from unittest import skip

# Url della vista scritto sia in modo diretto che in modo interno.
ID_PRESENTE = 1
URL = f"/acquisti/inserimento_cdc/{ID_PRESENTE}/"
REVERSE_URL = reverse('acquisti:inserimento_cdc', kwargs={'pk': ID_PRESENTE})


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        self.assertEquals(REVERSE_URL, URL)

    def test_inserisce_ordine_url_resolves_inserisce_ordine_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, inserimento_cdc)


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
    def test_redirection_to_login_for_not_logged_in_user(self):
        login_url = reverse('login')
        response = self.client.get(URL)
        self.assertRedirects(response, f'{login_url}?next={URL}')


class PermissionRequiredTests(MyAccountTestCase):
    def test_deny_for_logged_in_user_not_authorized_on_app(self):
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        response = self.client.get(URL)
        self.assertEquals(response.status_code, HTTP_403_FORBIDDEN)


class FormGeneralTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['af', 'cdc', 'azienda', 'fornitore', 'ordine_acquisto']
    
    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.ACQUISTI_ORDINI_INSERISCE, SiwPermessi.ACQUISTI_ORDINI_VIEW}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_page_structure(self):
        response = self.client.get(URL)
        # Controllo che il server risponda con ok.
        self.assertEquals(response.status_code, HTTP_200_OK)
        # Controllo che ci sia la parte di descrizione generale dell'ordine.
        self.assertContains(response, 'id_dettaglio_ordine')
        self.assertContains(response, 'Ordine di Prova')
        # Controllo che ci sia la parte della tabella delle ripartizioni.
        self.assertContains(response, 'id_lista_cdc_ripartizioni')
        self.assertContains(response, "Nessun CDC ancora assegnato")
        
    def test_csrf(self):
        response = self.client.get(URL)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        response = self.client.get(URL)
        form = response.context.get('form')
        self.assertIsInstance(form, RipartizioneForm)
    
    def test_render_with_correct_templates(self):
        response = self.client.get(URL)
        self.assertTemplateUsed(response, 'acquisti/inserisce_cdc.html')
    
    def test_new_ripartizione_100_con_dati_validi(self):
        # Inserisce una ripartizione. Uso dummy per il campo testuale che non viene usato in quanto setto direttamente
        # il cdc senza passare del controllo JQWidgets.
        # Impostando il 100% mi aspetto che vada poi direttamente ad ordini in quanto non posso inserirne altre.
        data = {'cdc': 4,
                'cdc_txt': 'dummy',
                'acquisto': 1,
                'percentuale_di_competenza': 100, }
        response = self.client.post(URL, data)
        # Controlla che sia stato inserito un record.
        self.assertTrue(RipartizioneSpesaPerCDC.objects.exists())
        # Lo recupera e verifica che sia stato generato il redirect alla pagina di inserimento dei centri di costo.
        ordine = RipartizioneSpesaPerCDC.objects.get(acquisto=1)
        self.assertIsInstance(ordine, RipartizioneSpesaPerCDC)
        # Controlla il redirect alla pagina di inserimento dei CDC.
        self.assertRedirects(response, reverse('acquisti:ordini'), HTTP_302_FOUND, HTTP_200_OK)
        # Apro la pagina della lista ordini e lo dovrei trovare.
        url = reverse('acquisti:ordini')
        response = self.client.get(url)
        self.assertContains(response, 'FAP')
        
    def test_new_ripartizione_50_con_dati_validi(self):
        # Inserisce una ripartizione. Uso dummy per il campo testuale che non viene usato in quanto setto direttamente
        # il cdc senza passare del controllo JQWidgets.
        # Impostando il 50% mi aspetto che rimanga sulla pagina di inserimento.
        data = {'cdc': 4,
                'cdc_txt': 'dummy',
                'acquisto': 1,
                'percentuale_di_competenza': 50, }
        response = self.client.post(URL, data)
        # Controlla che sia stato inserito un record.
        self.assertTrue(RipartizioneSpesaPerCDC.objects.exists())
        # Lo recupera e verifica che sia stato generato il redirect alla pagina di inserimento dei centri di costo.
        ordine = RipartizioneSpesaPerCDC.objects.get(acquisto=1)
        self.assertIsInstance(ordine, RipartizioneSpesaPerCDC)
        # Controlla il redirect alla pagina di inserimento dei CDC.
        self.assertRedirects(response, reverse('acquisti:inserimento_cdc',
                                               kwargs={'pk': ordine.id}), HTTP_302_FOUND, HTTP_200_OK)
        # Apro la pagina della lista ordini e lo dovrei trovare.
        url = reverse('acquisti:inserimento_cdc', kwargs={'pk': ordine.id})
        response = self.client.get(url)
        self.assertContains(response, 'FAP')
        
    @skip
    def test_new_acquisto_senza_dati(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        response = self.client.post(URL, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
