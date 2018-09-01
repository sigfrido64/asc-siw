# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinLengthValidator
from siw.siwmodels import SiwGeneralModel
from collaboratori.models import Collaboratore
from anagrafe.models import PersonaInAzienda
__author__ = "Pilone Ing. Sigfrido"


class IncarichiExtension(models.Model):
    """
            Campi per la gestione di sistema.
    """
    # Data da cui parto a considerare valido il record.
    valido_dal = models.DateField(verbose_name="Data di inizio validità")
    # Data in cui il record cessa di essere valido.
    valido_al = models.DateField(verbose_name="Data di fine validità")

    class Meta:
        abstract = True

    def incaricabile(self, data_inizio_incarico, data_fine_incarico):
        raise NotImplementedError("La classe deve definire questo metodo !")

    def costo_azienda(self, lista_pagamenti):
        raise NotImplementedError("La classe deve definire questo metodo !")


class Iniziativa(SiwGeneralModel):
    """
    Definizione delle iniziative
    """
    nome = models.CharField(
        unique=True, max_length=30, validators=[MinLengthValidator(3)],
        verbose_name="Nome sintetico dell'iniziativa")
    descrizione = models.CharField(
        max_length=120, validators=[MinLengthValidator(5)], verbose_name="Breve descrizione dell'iniziativa")
    
    cup = models.CharField(max_length=30, blank=True, verbose_name='CUP se presente')
    cig = models.CharField(max_length=30, blank=True, verbose_name='CIG se presente')
    iva_detraibile = models.BooleanField(
        default=True, verbose_name="L'IVA delle spese connesse all'iniziativa è scaricabile ?")
    
    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    # Data da cui parto a considerare valido il record.
    valido_dal = models.DateField(verbose_name="Data di inizio validità")
    # Data in cui il record cessa di essere valido.
    valido_al = models.DateField(verbose_name="Data di fine validità")
    # Data di aggiornamento del record.

    # META Class.
    class Meta:
        verbose_name = "Iniziativa"
        verbose_name_plural = "Iniziative"
        ordering = ['nome']

    # To String.
    def __str__(self):
        return self.nome + ' - ' + self.descrizione


class Progetto(SiwGeneralModel):
    """
    Definizione di un progetto
    """
    nome = models.CharField(
        unique=True, max_length=30, validators=[MinLengthValidator(3)],
        verbose_name="Nome sintetico del Progetto")
    descrizione = models.CharField(
        max_length=120, validators=[MinLengthValidator(5)], verbose_name="Breve descrizione del Progetto")
    # Iniziativa cui è correlato.
    iniziativa = models.ForeignKey(Iniziativa, on_delete=models.PROTECT)

    cup = models.CharField(max_length=30, blank=True, verbose_name='CUP se presente')
    cig = models.CharField(max_length=30, blank=True, verbose_name='CIG se presente')

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    # Data da cui parto a considerare valido il record.
    valido_dal = models.DateField(verbose_name="Data di inizio validità")
    # Data in cui il record cessa di essere valido.
    valido_al = models.DateField(verbose_name="Data di fine validità")

    # META Class.
    class Meta:
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"
        ordering = ['nome']

    # To String.
    def __str__(self):
        return self.iniziativa.nome + ' = > ' + self.nome + ' - ' + self.descrizione


class SottoProgetto(SiwGeneralModel):
    """
    Definizione di un sotto-progetto
    """
    nome = models.CharField(
        unique=True, max_length=30, validators=[MinLengthValidator(3)],
        verbose_name="Nome sintetico del Sotto-Progetto")
    descrizione = models.CharField(
        max_length=120, validators=[MinLengthValidator(5)], verbose_name="Breve descrizione del Sotto-Progetto")
    # Progetto cui è correlato.
    progetto = models.ForeignKey(Progetto, on_delete=models.PROTECT)

    cup = models.CharField(max_length=30, blank=True, verbose_name='CUP se presente')
    cig = models.CharField(max_length=30, blank=True, verbose_name='CIG se presente')

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    # Data da cui parto a considerare valido il record.
    valido_dal = models.DateField(verbose_name="Data di inizio validità")
    # Data in cui il record cessa di essere valido.
    valido_al = models.DateField(verbose_name="Data di fine validità")

    # META Class.
    class Meta:
        verbose_name = "Sotto-Progetto"
        verbose_name_plural = "Sotto Progetti"
        ordering = ['nome']

    # To String.
    def __str__(self):
        return self.progetto.iniziativa.nome + ' - > ' + self.progetto.nome + ' => ' + \
               self.nome + ' - ' + self.descrizione


class Occasionale(SiwGeneralModel, IncarichiExtension):
    """
    Definizione degli elementi amministrativi per i collaboratori occasionali.
    """
    collaboratore = models.OneToOneField(Collaboratore, on_delete=models.PROTECT)
    documenti_consegnati = models.BooleanField(default=False)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    class Meta:
        verbose_name = "Collaborazione Occasionale"
        verbose_name_plural = "Collaborazioni Occasionali"

    def incaricabile(self, data_inizio_incarico, data_fine_incarico):
        """
        devo dire se il collaboratore 
        :param data_inizio_incarico:
        :param data_fine_incarico:
        :return:
        """
        raise NotImplementedError("La classe deve definire questo metodo !")

    def costo_azienda(self, lista_pagamenti):
        raise NotImplementedError("La classe deve definire questo metodo !")

    def __str__(self):
        return self.collaboratore.persona.cognome + ' - ' + self.collaboratore.persona.nome


class Parasubordinato(SiwGeneralModel, IncarichiExtension):
    """
    Definizione degli elementi amministrativi per i collaboratori occasionali.
    """
    collaboratore = models.ForeignKey(Collaboratore, on_delete=models.PROTECT)
    documenti_consegnati = models.BooleanField(default=False)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    class Meta:
        verbose_name = "Collaborazione CoCoCo"
        verbose_name_plural = "Collaborazioni CoCoCo"

    def incaricabile(self, data_inizio_incarico, data_fine_incarico):
        """
        devo dire se il collaboratore
        :param data_inizio_incarico:
        :param data_fine_incarico:
        :return:
        """
        raise NotImplementedError("La classe deve definire questo metodo !")

    def costo_azienda(self, lista_pagamenti):
        raise NotImplementedError("La classe deve definire questo metodo !")

    def __str__(self):
        return self.collaboratore.persona.cognome + ' - ' + self.collaboratore.persona.nome


class Autonomo(SiwGeneralModel, IncarichiExtension):
    """
    Definizione degli elementi amministrativi per i collaboratori occasionali.
    """
    collaboratore = models.ForeignKey(Collaboratore, on_delete=models.PROTECT)
    personainazienda = models.ForeignKey(PersonaInAzienda, on_delete=models.PROTECT)
    documenti_consegnati = models.BooleanField(default=False)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    class Meta:
        verbose_name = "Collaborazione Autonoma"
        verbose_name_plural = "Collaborazioni Autonome"

    def incaricabile(self, data_inizio_incarico, data_fine_incarico):
        """
        devo dire se il collaboratore
        :param data_inizio_incarico:
        :param data_fine_incarico:
        :return:
        """
        raise NotImplementedError("La classe deve definire questo metodo !")

    def costo_azienda(self, lista_pagamenti):
        raise NotImplementedError("La classe deve definire questo metodo !")

    def __str__(self):
        return self.collaboratore.persona.cognome + ' - ' + self.collaboratore.persona.nome
