# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import ModelForm
from unittest import skip
from accounts.models import SiwPermessi
from siw.sig_debug import response_debug
__author__ = "Pilone Ing. Sigfrido"


URL = '/amm/cdc/'  # Questo è il link che ho scritto nelle urls per arrivare a questa vista.
REVERSE_URL = 'amm:cdc_home'  # Questa è la stringa che uso per il reverse per vedere che link genera.


class MyAccountTestCase(TestCase):
    """
    Qui metto le informazioni di base per i test successivi.
    Metto 'username' e 'passoword' e l'url della pagina che voglio testare come reverse
    """
    def setUp(self):
        # Fake user
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        # Dati dell'utente
        self.myuser = User.objects.get(username=self.username)
        # Link alla vista
        self.url = reverse(REVERSE_URL)


class LoginRequiredTests(MyAccountTestCase):
    # Test che faccio per un utente non loggato, un utente guest.
    def test_redirection(self):
        # Un utente non loggato deve essere rediretto alla pagina di login.
        login_url = reverse('login')
        response = self.client.get(self.url)
        response_debug(response)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class PermissionRequiredTests(MyAccountTestCase):
    # Qui metto i test per un utente che si logga ma che non ha i permessi per accedere all'app.
    def test_no_perms_on_app(self):
        # Un utente che si logga senza permessi e prova ad accere alla pagina dell'applicazione deve ricevere
        # come risposta 403 = Denied !
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 403)
        

class FormGeneralTests(MyAccountTestCase):
    # Qui metto i test per un utente che si logga e che ha i permessi per accedere.
    # Quindi qui metto tutti i test funzionali veri e propri in quanto i precedenti servono più che altro a
    # garantire che non si acceda senza permessi.
    def setUp(self):
        # Seup della classe dando i permessi all'utente.
        super().setUp()
        self.myuser.profile.permessi = {SiwPermessi.AMM_CDC_READ}
        self.myuser.save(force_update=True)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        # Il server riesce a fornire la pagina richiesta.
        self.assertEquals(self.response.status_code, 200)

    @skip
    def test_url_resolves_correct_view(self):
        # La risoluzione dell'url mi manda alla vista corretta.
        # Il test fallisce quando il link non mi porta alla vista e devi guardare negli urls dell'app.
        view = resolve(URL)
        self.assertEquals(view.func, mdl)
        
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


    """
    Testing : Accesso e visibilità della vista in ogni suo aspetto.
    
    ## Nei menù la vista esce solo se sono loggato e se ho i permessi
    
    
    
    # Creo l'utente base per le prove.
    def setUp(self):
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.myuser = User.objects.get(username=self.username)

    def test_logged_in_uses_correct_template_and_logout(self):
        # Provo ad accedere alla home senza loggarmi e mi deve rimandare al login con il next alla Home.
        resp = self.client.get(reverse('home'))
        self.assertRedirects(resp, '/login/?next=/')

        # Allora loggo l'utente.
        self.client.login(username='john', password='secret123')
        resp = self.client.get(reverse('home'))

        # Controllo che il login sia andato a buon fine.
        self.assertEqual(str(resp.context['user']), 'john', "Non sono riuscito a loggarmi")
        
        # Controllo che la risposta sia un 'success'
        self.assertEqual(resp.status_code, 200, "Non ho recuperato la pagina di login")

        # Controllo se viene usato il template corretto
        self.assertTemplateUsed(resp, 'home.html', "Non è stato usato il template corretto")
        
        # Controllo che nel testo ci sia la voce logout 'Esci'
        self.assertTrue(b'Esci' in resp.content, "Manca la voce per il Logout")

        # A questo punto logout.
        self.client.logout()

        # Controllo che la risposta sia un 'success'
        self.assertEqual(resp.status_code, 200, "Logout non andato a buon fine")
"""

"""


class SuccessfulMyAccountTests(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
        })

    def test_redirection(self):
        "
        A valid form submission should redirect the user
        "
        self.assertRedirects(self.response, self.url)

    def test_data_changed(self):
        ""
        refresh the user instance from database to get the updated data.
        ""
        self.user.refresh_from_db()
        self.assertEquals('John', self.user.first_name)
        self.assertEquals('Doe', self.user.last_name)
        self.assertEquals('johndoe@example.com', self.user.email)


class InvalidMyAccountTests(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {
            'first_name': 'longstring' * 100
        })

    def test_status_code(self):
        ""
        An invalid form submission should return to the same page
        ""
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

"""