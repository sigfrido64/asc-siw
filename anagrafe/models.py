# coding=utf-8
from django.db import models
from siw.context_processor import get_current_username

# Create your models here.
"""
Definizione dei modelli
"""


class Persona(models.Model):
    """
    Persone : Sono solo persone fisiche.

    Qui vado a memorizzare solo i dati personali. Quindi se poi li trovo definiti in qualche azienda i dati che trovo
    la sono relativi al loro recapito nelle varie aziende.
    """
    # Riferimenti agli altri database.
    # Assocam Anagrafica Persone -> Matricola Assocam
    asc_id = models.BigIntegerField(unique=True, default=None, null=True)
    asc_data_elemento = models.DateTimeField(null=True, blank=True)
    asc_data_aggiornamento = models.DateTimeField(null=True, blank=True)

    asc_ca_id = models.BigIntegerField(unique=True, default=None, null=True)   # Contatto azienda
    asc_ca_data_elemento = models.DateTimeField(null=True, blank=True)
    asc_ca_data_aggiornamento = models.DateTimeField(null=True, blank=True)

    r2k_id = models.BigIntegerField(unique=True, default=None, null=True)      # Matricola rete 2000
    r2k_data_elemento = models.DateTimeField(null=True, blank=True)
    r2k_data_aggiornamento = models.DateTimeField(null=True, blank=True)

    # Nome
    titolo = models.CharField(max_length=20, blank=True)
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    vip = models.BooleanField(default=False)

    # Luogo e data di nascita
    comune_nascita = models.CharField(max_length=50, blank=True)
    provincia_nascita = models.CharField(max_length=2, blank=True)
    stato_nascita = models.CharField(max_length=40, blank=True)
    data_nascita = models.DateField(null=True, blank=True)

    # Cittadinanza.
    cittadinanza = models.CharField(max_length=40, blank=True)

    # Sesso
    sesso = models.CharField(max_length=1)

    # Domicilio
    indirizzo_domicilio = models.CharField(max_length=50, blank=True)
    comune_domicilio = models.CharField(max_length=50, blank=True)
    cap_domicilio = models.CharField(max_length=5, blank=True)
    provincia_domicilio = models.CharField(max_length=2, blank=True)
    regione_domicilio = models.CharField(max_length=25, blank=True)
    stato_domicilio = models.CharField(max_length=25, blank=True)

    # Residenza
    indirizzo_residenza = models.CharField(max_length=50, blank=True)
    comune_residenza = models.CharField(max_length=50, blank=True)
    cap_residenza = models.CharField(max_length=5, blank=True)
    provincia_residenza = models.CharField(max_length=2, blank=True)
    regione_residenza = models.CharField(max_length=25, blank=True)
    stato_residenza = models.CharField(max_length=25, blank=True)

    # Codice Fiscale
    cf = models.CharField(max_length=16, blank=True)

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
        verbose_name = "Persona"
        verbose_name_plural = "Persone"
        ordering = ['cognome']

    # To String.
    def __str__(self):
        return self.cognome + ' - ' + self.nome

    # Override Save.
    # Set actual user for last_user.
    def save(self, *args, **kwargs):
        self.last_user = get_current_username()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class TipoTelefonoPersone(models.Model):
    descrizione_telefono = models.CharField(max_length=20)

    # META Class.
    class Meta:
        verbose_name = "Tipo Telefono"
        verbose_name_plural = "Tipi Telefono"

    # To String.
    def __str__(self):
        return self.descrizione_telefono

