# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import SiwPermessi
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_302_FOUND
from ..views import inserimento_cdc_web
from ..forms import RipartizioneWebForm
from ..models import RipartizioneAcquistoWebPerCDC


# Url della vista scritto sia in modo diretto che in modo interno.
ID_PRESENTE = 1
URL = f"/acquisti/inserimento_cdc_web/{ID_PRESENTE}/"
REVERSE_URL = reverse('acquisti:inserimento_cdc_web', kwargs={'pk': ID_PRESENTE})


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        self.assertEquals(REVERSE_URL, URL)

    def test_inserisce_ripartizione_web_url_resolves_inserisce_ripartizione_web_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, inserimento_cdc_web)
        

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
    # NON CARICO ripartizioni_web per cui nessun acquisto ne ha nei test !
    fixtures = ['af', 'cdc', 'acquisto_web']
    
    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.ACQUISTI_ORDINI_INSERISCE, SiwPermessi.ACQUISTI_ORDINI_VIEW}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_page_structure_ordine_web_senza_ripartizioni(self):
        response = self.client.get(URL)
        # Controllo che il server risponda con ok.
        self.assertEquals(response.status_code, HTTP_200_OK)
        # Controllo che ci sia la parte di descrizione generale dell'ordine.
        self.assertContains(response, 'id_dettaglio_ordine')
        self.assertContains(response, 'Cartucce per Stampante Epson')
        # Controllo che ci sia la parte della tabella delle ripartizioni.
        self.assertContains(response, 'id_lista_cdc_ripartizioni')
        
        # Chiamo la funzione AJAX che riporta la lista delle ripartizioni e la dovrei trovare.
        url = reverse('acquisti:ajax_lista_ripartizioni_per_ordine_web', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertContains(response, 'Nessun CDC ancora assegnato')
        
    def test_csrf(self):
        response = self.client.get(URL)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        response = self.client.get(URL)
        form = response.context.get('form')
        self.assertIsInstance(form, RipartizioneWebForm)
    
    def test_render_with_correct_templates(self):
        response = self.client.get(URL)
        self.assertTemplateUsed(response, 'acquisti/inserisce_ripartizione_su_cdc_per_web.html')
    
    def test_new_ripartizione_100_con_dati_validi(self):
        # Inserisce una ripartizione. Uso dummy per il campo testuale che non viene usato in quanto setto direttamente
        # il cdc senza passare del controllo JQWidgets.
        # Impostando il 100% mi aspetto che vada poi direttamente ad ordini WEB in quanto non posso inserirne altre.
        data = {'cdc': 4,
                'cdc_txt': 'dummy',
                'acquisto_web': 1,
                'percentuale_di_competenza': 100, }
        response = self.client.post(URL, data)
        # Controlla che sia stato inserito un record.
        self.assertTrue(RipartizioneAcquistoWebPerCDC.objects.exists())
        # Lo recupera e verifica che sia stato generato il redirect alla pagina di inserimento dei centri di costo.
        ripartizione = RipartizioneAcquistoWebPerCDC.objects.get(acquisto_web=1)
        self.assertIsInstance(ripartizione, RipartizioneAcquistoWebPerCDC)
        # Controlla il redirect alla pagina ordini in quanto 100% implica no altri CDC.
        self.assertRedirects(response, reverse('acquisti:ordini_web'), HTTP_302_FOUND, HTTP_200_OK)
        # Apro la pagina della lista ordini e lo dovrei trovare.
        url = reverse('acquisti:ordini_web')
        response = self.client.get(url)
        self.assertContains(response, 'FAP')

    def test_new_ripartizione_50_con_dati_validi(self):
        # Inserisce una ripartizione. Uso dummy per il campo testuale (cdc_txt) che non viene usato in quanto
        # setto direttamente il cdc senza passare del controllo JQWidgets.
        # Impostando il 50% mi aspetto che rimanga sulla pagina di inserimento.
        data = {'cdc': 4,
                'cdc_txt': 'dummy',
                'acquisto_web': 1,
                'percentuale_di_competenza': 50, }
        # Faccio riferimento ad un ordine che non ha ancora CDC assegnati.
        response = self.client.post(URL, data)
        # Controlla che sia stato inserito un record.
        self.assertTrue(RipartizioneAcquistoWebPerCDC.objects.exists())
        # Lo recupera e verifica che sia stato generato il redirect alla pagina di inserimento dei centri di costo.
        ripartizione = RipartizioneAcquistoWebPerCDC.objects.get(acquisto_web=1)
        self.assertIsInstance(ripartizione, RipartizioneAcquistoWebPerCDC)
        # Controlla il redirect alla pagina di inserimento dei CDC.
        self.assertRedirects(response, reverse('acquisti:inserimento_cdc_web',
                                               kwargs={'pk': 1}), HTTP_302_FOUND, HTTP_200_OK)
        
        # Chiamo la funzione AJAX che riporta la lista delle ripartizioni e la dovrei trovare.
        url = reverse('acquisti:ajax_lista_ripartizioni_per_ordine_web', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'FAP')
        
    def test_new_acquisto_senza_dati(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        response = self.client.post(URL, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
