# coding=utf-8
from django.db import models
from anagrafe.models import Persona
from siw.context_processor import get_current_username

# Create your models here.


class Collaboratore(models.Model):
    """
    Sono le schede dei vari collaboratori della Scuola.

    Qui vado a memorizzare solo i dati che posso usare per contattarli quando sono collaboratori della Scuola.
    """
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)

    # Recapiti telefonici
    tel1 = models.CharField(max_length=30, blank=True)
    tel2 = models.CharField(max_length=30, blank=True)
    tel3 = models.CharField(max_length=30, blank=True)
    tel4 = models.CharField(max_length=30, blank=True)
    doc_tel1 = models.CharField(max_length=20, blank=True)
    doc_tel2 = models.CharField(max_length=20, blank=True)
    doc_tel3 = models.CharField(max_length=20, blank=True)
    doc_tel4 = models.CharField(max_length=20, blank=True)

    # Indirizzi di posta elettronica
    mail1 = models.CharField(max_length=50, blank=True)
    mail2 = models.CharField(max_length=50, blank=True)
    doc_mail1 = models.CharField(max_length=20, blank=True)
    doc_mail2 = models.CharField(max_length=20, blank=True)

    # Campo note
    note = models.TextField(blank=True, verbose_name='Eventuali note')

    """
        Campi per la gestione di sistema.
    """
    # Il record è ancora in uso ?
    in_uso = models.BooleanField(db_index=True, default=True, verbose_name="Il record è tutt'ora in uso ?")
    # Data di aggiornamento del record.
    data_aggiornamento = models.DateTimeField(auto_now=True)
    # Data di creazione del record.
    data_creazione = models.DateTimeField(auto_now_add=True)
    # Utente che ha apportato l'ultima modifica.
    last_user = models.CharField(max_length=80, blank=True, default='')

    # META Class.
    class Meta:
        verbose_name = "Collaboratore"
        verbose_name_plural = "Collaboratori"

    # To String.
    def __str__(self):
        return self.persona.cognome + ' - ' + self.persona.nome

    # Override Save.
    # Set actual user for last_user.
    def save(self, *args, **kwargs):
        self.last_user = get_current_username()
        super().save(*args, **kwargs)  # Call the "real" save() method.
