# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import ModelForm
from unittest import skip
from accounts.models import SiwPermessi
from siw.sig_http_status import HTTP_403_FORBIDDEN, HTTP_200_OK
from siw.sig_debug import response_debug

from ..views import lista_collaboratori_view
__author__ = "Pilone Ing. Sigfrido"


# Url della vista scritto sia in modo diretto che in modo interno.
URL = "/collaboratori/anagrafica/lista/"
REVERSE_URL = 'collaboratori:lista_collaboratori'


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL)
        self.assertEquals(url, URL)

    def test_lista_collaboratori_url_resolves_lista_collaboratori_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, lista_collaboratori_view)


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi.
    Metto 'username' e 'passoword' e l'url della pagina che voglio testare come reverse
    """
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
        self.response = self.client.get(URL)
        self.assertEquals(self.response.status_code, HTTP_403_FORBIDDEN)


class FormGeneralTestsForLoggedInUsersWithPermissions(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    def setUp(self):
        # Chiamo il setup della classe madre così evito duplicazioni di codice.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.COLLABORATORI_LISTA_READ}
        self.myuser.save(force_update=True)
        self.client.login(username=self.fake_user_username, password=self.fake_user_password)
        self.response = self.client.get(URL)

    def test_server_serve_page_without_errors(self):
        self.assertEquals(self.response.status_code, HTTP_200_OK)

    def test_render_with_all_needed_and_correct_templates(self):
        self.assertTemplateUsed(self.response, 'collaboratori/lista_collaboratori.html')
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'includes/menu.html')

    def test_page_contain_correct_table_head(self):
        table_head = "<thead><tr><th>Cognome</th><th>Nome</th><th>Dettagli</th></tr></thead>"
        self.assertInHTML(table_head, self.response.content.decode('utf8'))

    def test_page_contain_known_collaborator(self):
        self.assertInHTML('Pace - Gaspare', self.response.content.decode('utf8'))

    def test_todo(self):
        self.fail("Va a finire i test !")
        # TODO Devo controllare che ci sia almeno un docente andando a definire delle Fixtures !

    @skip("In questa vista non sono presenti form per cui non c'è csrfmiddlewaretoken")
    def test_csrf(self):
        # Il crfmiddlewaretoken ci deve essere
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    @skip("In questa vista non sono presenti form per cui non c'è un form")
    def test_contains_form(self):
        # Devo avere un oggetto di tipo form
        form = self.response.context['form']
        self.assertIsInstance(form, ModelForm)

    @skip
    def test_use_template(self):
        # Controllo che usi il template corretto.
        self.assertTemplateUsed(self.response, 'attesta/mdl.html',
                                "Non è stato usato il template corretto")

    @skip
    def test_form_inputs(self):
        """
        La vista deve contenere :
        L'Anno Formativo, la data di stampa, la lista dei corsi, la lista delle stampe e la Tabella degli allievi.
        """
        self.assertContains(self.response, '<select id="anni_formativi"', 1)
        self.assertContains(self.response, '<input type="date" id="data_stampa"/>', 1)
        self.assertContains(self.response, '<select id="lista_corsi"', 1)
        self.assertContains(self.response, '<select id="lista_stampe"', 1)
        self.assertContains(self.response, '<tbody id="lista_allievi">', 1)


