# coding=utf-8
import re
from django.db import models
from django.core.exceptions import ValidationError

__author__ = "Pilone Ing. Sigfrido"


class AnnoFormativo(models.Model):
    anno_formativo = models.CharField(max_length=12, unique=True)
    default = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Anno Formativo"
        verbose_name_plural = "Anni Formativi"

    def __str__(self):
        return self.anno_formativo

    # Custon Check fields.
    def clean(self):
        # L'Anno Formativo deve essere nella forma AF 2018-2019 ed in maiuscolo.
        # Lo porto in maiuscolo.
        self.anno_formativo = self.anno_formativo.upper()
        # Estraggo anno di inizio e di fine.
        mo = re.search(r'AF (?P<inizio>\d{4})-(?P<fine>\d{4})', self.anno_formativo)
        inizio = int(mo.group('inizio'))
        fine = int(mo.group('fine'))
        if inizio < 2000:
            raise ValidationError({'anno_formativo': "L'anno d'inizio deve essere maggiore di 2000 "})
        if fine != inizio + 1:
            raise ValidationError({'anno_formativo': "L'anno di fine deve essere quello seguente a quello d'inizio"})
