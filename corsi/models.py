# coding=utf-8
from django.db import models
from siw.siwmodels import SiwGeneralModel
from amm.models import CentroDiCosto


def date_to_int(data):
    return data.year * 1000 + data.timetuple().tm_yday


class OrdineProduzione(SiwGeneralModel):
    """
    Definisce l'ordine di produzione per i corsi.
    """
    numero_ordine = models.CharField(max_length=10, unique=True)

    # Almeno uno di loro deve essere valorizzato !
    cdc = models.ForeignKey(CentroDiCosto, on_delete=models.PROTECT, blank=True, null=True)

    data_inizio = models.DateField()
    data_inizio_annodoy = models.IntegerField(default=0)
    data_fine = models.DateField()
    data_fine_annodoy = models.IntegerField(default=0)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    def __str__(self):
        return self.numero_ordine

    # Custon Check fields.
    def clean(self):
        raise NotImplementedError("E qui cosa devo controllare ?")


class Corso(SiwGeneralModel):
    """
    Definizione del corso
    TODO Devo definire degli stati per permettere di gestire il catalogo, la bozza, e poi il corso vero e proprio
    con un relativo stato.

    annodoy lo devo scrivere quando salvo
    in admin
    deve essere visualizzato ma di sola lettura.
    """
    codice_edizione = models.CharField(primary_key=True, max_length=10)
    denominazione = models.CharField(max_length=150)
    durata = models.IntegerField(default=8)
    cdc = models.ForeignKey(CentroDiCosto, on_delete=models.PROTECT, blank=True, null=True)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    # Campi compilati durante il salvataggio.
    data_inizio = models.DateField()
    data_inizio_annodoy = models.IntegerField(default=0)
    data_fine = models.DateField()
    data_fine_annodoy = models.IntegerField(default=0)

    # META Class.
    class Meta:
        verbose_name = "Corso"
        verbose_name_plural = "Corsi"

    def __str__(self):
        return self.codice_edizione + ' - ' + self.denominazione

    # Override Save.
    def save(self, *args, **kwargs):
        # Aggiorna ad "anno + numero del giorno da gennaio" che mi è utile per poi semplificare le query
        self.data_inizio_annodoy = date_to_int(self.data_inizio)
        self.data_fine_annodoy = date_to_int(self.data_fine)
        super().save(*args, **kwargs)
