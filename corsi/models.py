# coding=utf-8
from django.db import models
from siw.siwmodels import SiwGeneralModel
from amm.models.centri_di_costo import CentroDiCosto


def date_to_int(data):
    # anno + numero del giorno da gennaio
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
    # TODO
    # Il cdc deve avere lo stesso nome del corso. Da mettere nel metodo clean.
    BOZZA = 0
    IN_SVOLGIMENTO = 50
    TERMINATO = 100
    CHIUSO = 150
    STATO_CORSO_CHOICES = (
        (BOZZA, 'Bozza'),
        (IN_SVOLGIMENTO, 'In Svolgimento'),
        (TERMINATO, 'Terminato'),
        (CHIUSO, 'Chiuso')
    )

    codice_edizione = models.CharField(primary_key=True, max_length=10)
    denominazione = models.CharField(max_length=150)
    durata = models.FloatField(default=8)
    cdc = models.ForeignKey(CentroDiCosto, on_delete=models.PROTECT, blank=True, null=True)
    stato_corso = models.IntegerField(choices=STATO_CORSO_CHOICES, default=BOZZA)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    # Date di inizio e fine corso.
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
