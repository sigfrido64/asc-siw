# coding=utf-8
from django.test import TestCase
from ..forms import SignUpForm


# Controlla che il form contenga i campi minimi che mi aspetto.
class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
