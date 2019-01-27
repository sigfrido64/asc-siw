# coding=utf-8
from django.db import models
from siw.context_processor import get_current_username, set_current_username


class SiwGeneralModel(models.Model):
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

    class Meta:
        abstract = True

    def clean(self):
        set_current_username('pippo')

    # Override Save.
    # Set actual user for last_user.
    def save(self, *args, **kwargs):
        self.last_user = get_current_username()
        super().save(*args, **kwargs)
