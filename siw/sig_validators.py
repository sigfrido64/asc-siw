# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.core.exceptions import ValidationError

__all__ = {'percentuale_maggiore_zero'}


def percentuale_maggiore_zero(value):
    if value <= 0 or value > 100:
        raise ValidationError('Le percentuali devono essere maggiori di 0 e minori di 100', code='invalid')
