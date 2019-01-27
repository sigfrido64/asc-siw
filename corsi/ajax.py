# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from .models import Corso
from siw.sig_utils import from_choices_to_list


def ajax_lista_stati_corso(request):
    stati_corso = Corso.STATO_CORSO_CHOICES
    return from_choices_to_list(stati_corso)
