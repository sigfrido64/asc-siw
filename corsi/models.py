# coding=utf-8
from django.db import models
from siw.siwmodels import SiwGeneralModel
from amm.models import CentroDiCosto


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
    """
    codice_edizione = models.CharField(primary_key=True, max_length=10)
    denominazione = models.CharField(max_length=150)
    durata = models.IntegerField(default=8)

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

    # Override Save.
    # Set annodoy per data_inizio e data_fine
    def save(self, *args, **kwargs):
        day_of_year = self.data_inizio.year * 1000 + self.data_inizio.timetuple().tm_yday
        print("Mi è venuto fuori questo : ", day_of_year)
        print("Mentre il monotono è : ", self.data_inizio.monotonic())
        self.data_inizio_annodoy = self.data_inizio
        raise NotADirectoryError("Devi finire di implementare il save qui !")
        super().save(*args, **kwargs)
