# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinLengthValidator
from siw.context_processor import get_current_username
__author__ = "Pilone Ing. Sigfrido"


class Iniziativa(models.Model):
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

    """
        Campi per la gestione di sistema.
    """
    # Il record è ancora in uso ?
    in_uso = models.BooleanField(db_index=True, default=True, verbose_name="Il record è tutt'ora in uso ?")
    # Data da cui parto a considerare valido il record.
    valido_dal = models.DateField(verbose_name="Data di inizio validità")
    # Data in cui il record cessa di essere valido.
    valido_al = models.DateField(verbose_name="Data di fine validità")
    # Data di aggiornamento del record.
    data_aggiornamento = models.DateTimeField(auto_now=True)
    # Data di creazione del record.
    data_creazione = models.DateTimeField(auto_now_add=True)
    # Utente che ha apportato l'ultima modifica.
    last_user = models.CharField(max_length=80, blank=True, default='')

    # META Class.
    class Meta:
        verbose_name = "Iniziativa"
        verbose_name_plural = "Iniziative"
        ordering = ['nome']

    # To String.
    def __str__(self):
        return self.nome + ' - ' + self.descrizione

    # Override Save.
    # Set actual user for last_user.
    def save(self, *args, **kwargs):
        self.last_user = get_current_username()
        print('user : ' + get_current_username())
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Progetto(models.Model):
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

    """
        Campi per la gestione di sistema.
    """
    # Il record è ancora in uso ?
    in_uso = models.BooleanField(db_index=True, default=True, verbose_name="Il record è tutt'ora in uso ?")
    # Data da cui parto a considerare valido il record.
    valido_dal = models.DateField(verbose_name="Data di inizio validità")
    # Data in cui il record cessa di essere valido.
    valido_al = models.DateField(verbose_name="Data di fine validità")
    # Data di aggiornamento del record.
    data_aggiornamento = models.DateTimeField(auto_now=True)
    # Data di creazione del record.
    data_creazione = models.DateTimeField(auto_now_add=True)
    # Utente che ha apportato l'ultima modifica.
    last_user = models.CharField(max_length=80, blank=True, default='')

    # META Class.
    class Meta:
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"
        ordering = ['nome']

    # To String.
    def __str__(self):
        return self.iniziativa.nome + ' = > ' + self.nome + ' - ' + self.descrizione

    # Override Save.
    # Set actual user for last_user.
    def save(self, *args, **kwargs):
        self.last_user = get_current_username()
        print('user : ' + get_current_username())
        super().save(*args, **kwargs)  # Call the "real" save() method.


class SottoProgetto(models.Model):
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

    """
        Campi per la gestione di sistema.
    """
    # Il record è ancora in uso ?
    in_uso = models.BooleanField(db_index=True, default=True, verbose_name="Il record è tutt'ora in uso ?")
    # Data da cui parto a considerare valido il record.
    valido_dal = models.DateField(verbose_name="Data di inizio validità")
    # Data in cui il record cessa di essere valido.
    valido_al = models.DateField(verbose_name="Data di fine validità")
    # Data di aggiornamento del record.
    data_aggiornamento = models.DateTimeField(auto_now=True)
    # Data di creazione del record.
    data_creazione = models.DateTimeField(auto_now_add=True)
    # Utente che ha apportato l'ultima modifica.
    last_user = models.CharField(max_length=80, blank=True, default='')

    # META Class.
    class Meta:
        verbose_name = "Sotto-Progetto"
        verbose_name_plural = "Sotto Progetti"
        ordering = ['nome']

    # To String.
    def __str__(self):
        return self.progetto.iniziativa.nome + ' - > ' + self.progetto.nome + ' => ' + \
               self.nome + ' - ' + self.descrizione

    # Override Save.
    # Set actual user for last_user.
    def save(self, *args, **kwargs):
        self.last_user = get_current_username()
        print('user : ' + get_current_username())
        super().save(*args, **kwargs)  # Call the "real" save() method.