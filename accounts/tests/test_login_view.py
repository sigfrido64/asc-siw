# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginViewTest(TestCase):
    """
    Testing : Login e Logout
    In questo test case controllo che il login venga richiesto per accedere alla home page se non sono loggato e che
    il logout mi riporti alla pagina di login con il next alla home.
    """
    fixtures = ['af']
    
    # Crea l'utente per le prove.
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
