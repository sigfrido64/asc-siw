# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import SiwPermessi
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_302_FOUND
from ..views import ordine_modifica
from ..forms import AcquistoConOrdineForm
from ..models import AcquistoConOrdine

from unittest import skip

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
        
    @skip("Ed uno")
    def test_new_acquisto_con_dati_validi(self):
        # Inserisce un ordine.
        data = {'numero_protocollo': 1,
                'data_ordine': '2018-11-13',
                'stato': AcquistoConOrdine.STATO_BOZZA,
                'tipo': AcquistoConOrdine.TIPO_ORDINE_A_FORNITORE,
                'fornitore': ['1'],
                'descrizione': 'Prova di ordine che inserisco',
                'imponibile': 1000,
                'aliquota_IVA': 22,
                'percentuale_IVA_indetraibile': 50, }
        response = self.client.post(URL, data)
        # Controlla che sia stato inserito un record.
        self.assertTrue(AcquistoConOrdine.objects.exists())
        # Lo recupera e verifica che sia stato generato il redirect alla pagina di inserimento dei centri di costo.
        ordine = AcquistoConOrdine.objects.get(descrizione='Prova di ordine che inserisco')
        # Controlla il redirect alla pagina di inserimento dei CDC.
        self.assertRedirects(response, reverse('acquisti:inserimento_cdc',
                                               kwargs={'pk': ordine.id}), HTTP_302_FOUND, HTTP_200_OK)
        
        # Apro la pagina della lista ordini e lo dovrei trovare.
        url = reverse('acquisti:ordini')
        response = self.client.get(url)
        self.assertContains(response, 'Prova di ordine che inserisco')

    @skip("E due")
    def test_new_acquisto_senza_dati(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        response = self.client.post(URL, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
    
    @skip("E tre")
    def test_1(self):
        """
        se modifico imponibile deve aggiornare le ripartizioni ed il costo totale se c'è.
        :return:
        """
        self.fail("Vai a finire i test")

    @skip
    def test_2(self):
        """
        se la ripartizioni non arrivano al 100% devo riaprire la maschera delle ripartizioni.
        :return:
        """
        self.fail("Vai a finire i test")
