# coding=utf-8
from django.db import models

from siw.siwmodels import SiwGeneralModel
from collaboratori.models import Collaboratore
from corsi.models import Corso
from amm.models.mixins import AnnoFormativo
__author__ = "Pilone Ing. Sigfrido"


class IncaricoDocenza(SiwGeneralModel):
    OCCASIONALE = 0
    COCOCO = 1
    AUTONOMO = 2
    DIPENDENTE = 3
    COLLABORATORE_CHOICES = (
        (OCCASIONALE, 'Occasionale'),
        (COCOCO, 'CoCoCo/CoCoPro'),
        (AUTONOMO, 'Autonomo'),
        (DIPENDENTE, 'Dipendente')
    )

    BOZZA = 0
    EMESSO = 1
    FIRMATO = 2
    IN_CORSO = 3
    CHIUSO = 4
    LIQUIDATO = 5
    STATO_INCARICO_CHOICES = (
        (BOZZA, 'Bozza'),
        (EMESSO, 'Emesso'),
        (FIRMATO, 'Firmato'),
        (IN_CORSO, 'In Corso'),
        (CHIUSO, 'Chiuso'),
        (LIQUIDATO, 'Liquidato')
    )

    anno_formativo = models.ForeignKey(AnnoFormativo, on_delete=models.PROTECT)
    stato_incarico = models.IntegerField(choices=STATO_INCARICO_CHOICES, default=BOZZA)
    numero = models.CharField(max_length=10, unique=True)

    data_incarico = models.DateField(auto_now=True)
    data_inizio_incarico = models.DateField(auto_now=True)
    data_termine_incarico = models.DateField(auto_now=True)

    collaboratore = models.ForeignKey(Collaboratore, on_delete=models.PROTECT)
    tipologia_collaboratore = models.IntegerField(choices=COLLABORATORE_CHOICES, default=None)

    corso = models.ForeignKey(Corso, on_delete=models.PROTECT)

    materia = models.CharField(max_length=80)

    ore_previste = models.FloatField()
    ore_effettive = models.FloatField(default=0)

    parametro_orario = models.FloatField()
    aggiuntivo_corso = models.FloatField(default=0)
    
    rimborso_spese_previsto = models.FloatField(default=0)
    rimborso_spese_effettivo = models.FloatField(default=0)

    importo_incarico_previsto = models.FloatField()
    importo_incarico_effettivo = models.FloatField(default=0)

    costo_incarico_previsto = models.FloatField()
    costo_incarico_effettivo = models.FloatField(default=0)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    class Meta:
        verbose_name = "Incarico di Docenza"
        verbose_name_plural = "Incarichi di Docenza"

    def __str__(self):
        return self.corso.codice_edizione + ' - ' + self.collaboratore.persona.__str__()

    # Override Save.
    # Set actual user for last_user.
    def save(self, *args, **kwargs):
        self.importo_incarico_previsto = self.ore_previste * self.parametro_orario + self.aggiuntivo_corso
        # TODO qui devo usare il calcolo del costo da tipo di incarico amministrativo !
        self.costo_incarico_previsto = self.importo_incarico_previsto * 1.2 + self.rimborso_spese_previsto
        super().save(*args, **kwargs)


class RilevamentoDocenza(SiwGeneralModel):
    """
    TODO La rilevazione delle ore deve dire solo le ore ed il periodo i in cui sono state effettuate. Meglio se puntuale ?
    
    Dopo devo convertire la rilevazione in una parte amministrativa in cui metto anche la parte di rimborso aggiuntibo
    ed eventualmente le spese sostenute.
    
    """
    incarico_docenza = models.ForeignKey(IncaricoDocenza, on_delete=models.PROTECT)
    ore_rilevate = models.IntegerField()
    # importo_aggiuntivo = models.FloatField(default=0)
    # rimborso_spese = models.FloatField(default=0)
    
    data_rilevazione = models.DateField(auto_now=True)

    importo_da_liquidare = models.FloatField()
    data_pagamento = models.DateField(auto_now=True)


class IncaricoAttivitaVarie(SiwGeneralModel):
    DOCENZA = 'D'
    ATTIVITA_VARIE = 'V'
    INCARICO_CHOICES = (
        (DOCENZA, 'Docenza'),
        (ATTIVITA_VARIE, 'Attività Varie diverse dalla Docenza'),
    )
    numero = models.IntegerField()
    data_incarico = models.DateField(auto_now=True)
    data_inizio_incarico = models.DateField(auto_now=True)
    data_termine_incarico = models.DateField(auto_now=True)
    collaboratore = models.ForeignKey(Collaboratore, on_delete=models.PROTECT)
