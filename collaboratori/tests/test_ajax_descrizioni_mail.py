# coding=utf-8
from django.test import TestCase
from django.urls import reverse, resolve
from siw.sig_http_status import HTTP_200_OK
from ..ajax import ajax_tipi_mail_persone


# Url della vista scritto sia in modo diretto che in modo interno.
URL = f"/collaboratori/ajax/lista_tipo_mail_persona/"
REVERSE_URL = 'collaboratori:ajax_lista_tipo_mail_persona'

"""
A T T E N Z I O N E

Qui non mi preoccupo di essere loggato perchè si tratta di informazioni che non hanno alcuna rilevanza.
"""


class GeneralTests(TestCase):
    def test_url_and_reverseurl_equality(self):
        url = reverse(REVERSE_URL)
        self.assertEquals(url, URL)

    def test_tipo_mail_url_resolves_tipo_mail_view(self):
        view = resolve(URL)
        self.assertEquals(view.func, ajax_tipi_mail_persone)


class TestsCorrectResponseLoginIndipendent(TestCase):
    fixtures = ['collaboratori.json']

    def setUp(self):
        self.response = self.client.get(URL)

    def test_server_serve_page_without_errors(self):
        self.assertEquals(self.response.status_code, HTTP_200_OK)

    def test_lista_tipi_telefoni(self):
        self.assertContains(self.response, 'Abitazione')
        self.assertContains(self.response, 'Lavoro')
