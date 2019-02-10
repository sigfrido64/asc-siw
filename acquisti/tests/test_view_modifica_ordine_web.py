# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms.models import model_to_dict
from accounts.models import SiwPermessi
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_302_FOUND
from ..views import ordine_modifica
from ..forms import AcquistoConOrdineForm
from ..models import AcquistoConOrdine

# Url della vista scritto sia in modo diretto che in modo interno.
URL = f"/acquisti/modifica_ordine/"
REVERSE_URL = 'acquisti:ordine_modifica'


class GeneralTests(TestCase):
    def setUp(self):
        chiave = 1
        self.url = URL + str(chiave) + '/'
        self.reverse_url = reverse(REVERSE_URL, kwargs={'pk': chiave})
        
    def test_url_and_reverseurl_equality(self):
        self.assertEquals(self.url, self.reverse_url)

    def test_modifica_ordine_url_resolves_modifica_ordine_view(self):
        view = resolve(self.url)
        self.assertEquals(view.func, ordine_modifica)
        self.fail("Da fare")


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
        # Creo un url valido.
        chiave = 1
        self.url = URL + str(chiave) + '/'


class LoginRequiredTests(MyAccountTestCase):
    def test_redirection_to_login_for_not_logged_in_user(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class PermissionRequiredTests(MyAccountTestCase):
    def test_deny_for_logged_in_user_not_authorized_on_app(self):
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, HTTP_403_FORBIDDEN)


class FormGeneralTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['af', 'cdc', 'azienda', 'fornitore', 'ordine_acquisto', 'ripartizioni']
    
    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.ACQUISTI_ORDINI_MODIFICA, SiwPermessi.ACQUISTI_ORDINI_VIEW}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_server_serve_page_without_errors(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, HTTP_200_OK)
        
    def test_csrf(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_contains_form(self):
        response = self.client.get(self.url)
        form = response.context.get('form')
        self.assertIsInstance(form, AcquistoConOrdineForm)

    def test_render_with_correct_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'acquisti/inserisce_modifica_ordine.html')
        

class FormSpecificTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    fixtures = ['af', 'cdc', 'azienda', 'fornitore', 'ordine_acquisto', 'ripartizioni']
    
    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.ACQUISTI_ORDINI_MODIFICA, SiwPermessi.ACQUISTI_ORDINI_VIEW,
                                        SiwPermessi.ACQUISTI_ORDINI_INSERISCE}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)

    def test_modifica_imponibile_modifica_ripartizioni_e_costo_totale(self):
        # Prendo il primo ordine.
        ordine = AcquistoConOrdine.objects.get(pk=1)
        # Porto l'imponibile a 2000
        ordine.imponibile = 2000
    
        # Creo i dati per la modifica del form e lancio la modifica.
        data = model_to_dict(ordine)
        response = self.client.post(self.url, data)
    
        # Recupero l'ordine dal data base.
        ordine = AcquistoConOrdine.objects.get(pk=1)
    
        # Controllo che l'imponibile sia diventato 2000
        self.assertEqual(ordine.imponibile, 2000)
        # Controllo che il costo totale sia 2440 (i due cdc sono ad IVA indetraibile)
        self.assertEqual(ordine.costo, 2440)

    def test_modifica_ordine_rimanda_a_ripartizione_se_non_ripartizione_completa(self):
        # Prendo il secondo ordine, che non ha ripartizioni.
        ordine = AcquistoConOrdine.objects.get(pk=2)
        # Porto l'imponibile a 2000, solo per avere qualche cosa da modificare.
        ordine.imponibile = 2000
    
        # Creo i dati per la modifica del form e lancio la modifica.
        data = model_to_dict(ordine)
        url = URL + str(2) + '/'
        response = self.client.post(url, data)
    
        # Controllo che mi abbia rimandato alla maschera di modifica degli ordini.
        self.assertRedirects(response, reverse('acquisti:inserimento_cdc', kwargs={'pk': 2}),
                             HTTP_302_FOUND, HTTP_200_OK)

