# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from siw.siwmodels import SiwGeneralModel
from anagrafe.models import Fornitore
from amm.models.centri_di_costo import CentroDiCosto
from amm.models.mixins import AnnoFormativo

# Tipo di spesa.
ACQUISTO_STANDARD = 1
ACQUISTO_WEB = 2


def _base(chiave, tipo):
    """
    Ritorna il queryset del tipo richiesto per i calcoli.
    :param pk: Chiave primaria del record correlato.
    :param tipo: Tipo di spesa.
    :return: Queryset relativo di chiave di correlazione 'chiave'.
    """
    if tipo == ACQUISTO_STANDARD:
        return RipartizioneSpesaPerCDC.objects.filter(acquisto=chiave)


def _aggiorna_ripartizioni_se_presenti(chiave, tipo):
    """
    Aggiorna le ripartizioni dei costi se sono già presenti.
    :param chiave: Chiave primaria del record correlato.
    :param tipo: Tipo di spesa.
    :return: None
    """
    ripartizioni = _base(chiave, tipo)
    for ripartizione in ripartizioni:
        ripartizione.save()

        
def _calcola_costo_totale(chiave, tipo):
    """"
    Calcola il costo totale di una spesa se sono presenti tutte le ripartizioni.
    :param pk: Chiave primaria del record correlato.
    :param tipo : Tipo di spesa.
    :return: None
    """
    base = _base(chiave, tipo)
    if somma_delle_ripartizioni(chiave, tipo) != 100:
        return True, None, None
    # Sommo i costi delle ripartizioni per fare il conto di quanto costa la singola spesa
    ripartizioni = base
    ripartizioni = ripartizioni.aggregate(Sum('costo_totale'))
    costo = ripartizioni['costo_totale__sum']
    # Infine compilo la stringa dei centri di costo.
    ripartizioni = base
    linea = ''
    for ripartizione in ripartizioni:
        token = str(ripartizione.percentuale_di_competenza) + '% ' + ripartizione.cdc.nome
        linea = linea + ', ' + token if linea else token
    return False, costo, linea


def somma_delle_ripartizioni(chiave, tipo):
    # Calcolo la somma delle ripartizioni di una data spesa.
    percentuali = _base(chiave, tipo)
    percentuali = percentuali.only('percentuale_di_competenza')
    percentuali = percentuali.aggregate(Sum('percentuale_di_competenza'))
    return percentuali['percentuale_di_competenza__sum'] if percentuali['percentuale_di_competenza__sum'] else 0


class AcquistoConOrdine(SiwGeneralModel):
    # Definizione degli stati
    STATO_BOZZA = 0
    STATO_DA_AUTORIZZARE = 10
    STATO_AUTORIZZATO = 20
    STATO_INVIATO = 30
    STATO_EVASO = 40
    STATO_CONFORME = 50
    STATO_LIQUIDATO = 60
    STATO_CHIUSO = 1000
    STATO_ANNULLATO = 900
    STATO_ORDINE_CHOICES = (
        (STATO_BOZZA, 'Bozza'),
        (STATO_DA_AUTORIZZARE, 'Da Autorizzare'),
        (STATO_AUTORIZZATO, 'Autorizzato'),
        (STATO_INVIATO, 'Inviato'),
        (STATO_EVASO, 'Evaso'),
        (STATO_CONFORME, 'Conforme'),
        (STATO_LIQUIDATO, 'Liquidato'),
        (STATO_CHIUSO, 'Chiuso'),
        (STATO_ANNULLATO, 'ANNULLATO'),
    )
    
    # Definizione del tipo di acquisto
    TIPO_ORDINE_A_FORNITORE = 10
    TIPO_ORDINE_CHOICES = (
        (TIPO_ORDINE_A_FORNITORE, 'Acquisto con Ordine a Fornitore'),
    )

    anno_formativo = models.ForeignKey(AnnoFormativo, on_delete=models.PROTECT)
    numero_protocollo = models.CharField(max_length=10, blank=True, unique=True, null=True, default=None)
    data_ordine = models.DateField()
    
    stato = models.IntegerField(choices=STATO_ORDINE_CHOICES, default=STATO_BOZZA)
    tipo = models.IntegerField(choices=TIPO_ORDINE_CHOICES)
    
    # Descrizione e fornitore
    fornitore = models.ForeignKey(Fornitore, on_delete=models.PROTECT)
    descrizione = models.TextField()
    
    # Dati economici dell'acquisto.
    imponibile = models.DecimalField(max_digits=7, decimal_places=2)
    aliquota_IVA = models.DecimalField(max_digits=4, decimal_places=2)
    percentuale_IVA_indetraibile = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    
    # Dati per la gestione successiva all'emissione dell'ordine.
    protocollo_fattura_fornitore = models.CharField(max_length=10, blank=True)
    conforme = models.BooleanField(default=False)
    
    note = models.TextField(blank=True)

    # Campi di sistema per garantire che le voci ordini vengano completate.
    dirty = models.BooleanField(default=True)
    iva_comunque_indetraibile = models.DecimalField(max_digits=7, decimal_places=2)
    iva_potenzialmente_detraibile = models.DecimalField(max_digits=7, decimal_places=2)
    cdc_verbose = models.CharField(null=True, max_length=50)
    costo = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    class Meta:
        verbose_name = "Acquisto"
        verbose_name_plural = "Acquisti"
        
    def __str__(self):
        return self.descrizione
    
    def clean(self):
        # Se stato BOZZA il protocollo è assente.
        if self.stato == self.STATO_BOZZA:
            self.numero_protocollo = None
        if self.numero_protocollo is None and self.stato != self.STATO_BOZZA:
            raise ValidationError(
                {'numero_protocollo': "Il numero di protocollo è obbligatorio per stati diversi da BOZZA"})

    # Override Save.
    def save(self, *args, **kwargs):
        # TODO : Dovrei controllare se il campo impobibile o le IVE (detraibile o no sono cambiate) prima di fare questo
        #        conto in aggiornamento.
        # Calcola l'IVA potenzialmente detraibile e quella comunque indetraibile.
        self.iva_comunque_indetraibile = self.imponibile * self.aliquota_IVA * self.percentuale_IVA_indetraibile / 10000
        self.iva_potenzialmente_detraibile = self.imponibile * self.aliquota_IVA / 100 - self.iva_comunque_indetraibile
        self.dirty = True
        super().save(*args, **kwargs)

        # Se ci sono già delle ripartizioni le aggiorna con i nuovi valori.
        # TODO : Anche questo lo dovrei fare solo se ho aggiornato qualche cosa che tocca questi campi. Da vedere dopo.
        _aggiorna_ripartizioni_se_presenti(self.pk, ACQUISTO_STANDARD)
        
    def calcola_costo_totale(self):
        self.dirty, self.costo, self.cdc_verbose = _calcola_costo_totale(self.pk, ACQUISTO_STANDARD)
        self.save()
        
    def aggiorna_ripartizioni(self):
        ripartizioni = RipartizioneSpesaPerCDC.objects.filter(acquisto=self.id)
        for ripartizione in ripartizioni:
            ripartizione.save(force_update=True)


class AcquistoSuWeb(SiwGeneralModel):
    # Definizione degli stati
    STATO_BOZZA = 0
    STATO_DA_AUTORIZZARE = 10
    STATO_AUTORIZZATO = 20
    STATO_INVIATO = 30
    STATO_EVASO = 40
    STATO_CONFORME = 50
    STATO_LIQUIDATO = 60
    STATO_CHIUSO = 1000
    STATO_ANNULLATO = 900
    STATO_ORDINE_CHOICES = (
        (STATO_BOZZA, 'Bozza'),
        (STATO_DA_AUTORIZZARE, 'Da Autorizzare'),
        (STATO_AUTORIZZATO, 'Autorizzato'),
        (STATO_INVIATO, 'Inviato'),
        (STATO_EVASO, 'Evaso'),
        (STATO_CONFORME, 'Conforme'),
        (STATO_LIQUIDATO, 'Liquidato'),
        (STATO_CHIUSO, 'Chiuso'),
        (STATO_ANNULLATO, 'ANNULLATO'),
    )
    
    anno_formativo = models.ForeignKey(AnnoFormativo, on_delete=models.PROTECT)
    numero_protocollo = models.CharField(max_length=10, blank=True, unique=True, null=True, default=None)
    data_ordine = models.DateField()
    
    stato = models.IntegerField(choices=STATO_ORDINE_CHOICES, default=STATO_BOZZA)
    
    # Descrizione
    descrizione = models.TextField()
    
    # Dati economici dell'acquisto.
    imponibile = models.DecimalField(max_digits=7, decimal_places=2)
    aliquota_IVA = models.DecimalField(max_digits=4, decimal_places=2)
    percentuale_IVA_indetraibile = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    
    # Dati per la gestione successiva all'emissione dell'ordine.
    protocollo_fattura_fornitore = models.CharField(max_length=10, blank=True)
    conforme = models.BooleanField(default=False)
    
    note = models.TextField(blank=True)
    
    # Campi di sistema per garantire che le voci ordini vengano completate.
    dirty = models.BooleanField(default=True)
    iva_comunque_indetraibile = models.DecimalField(max_digits=7, decimal_places=2)
    iva_potenzialmente_detraibile = models.DecimalField(max_digits=7, decimal_places=2)
    cdc_verbose = models.CharField(null=True, max_length=50)
    costo = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    
    class Meta:
        verbose_name = "Acquisto su Web"
        verbose_name_plural = "Acquisti su Web"
    
    def __str__(self):
        return self.descrizione
    
    def clean(self):
        # Se stato BOZZA il protocollo è assente.
        if self.stato == self.STATO_BOZZA:
            self.numero_protocollo = None
        if self.numero_protocollo is None and self.stato != self.STATO_BOZZA:
            raise ValidationError(
                {'numero_protocollo': "Il numero di protocollo è obbligatorio per stati diversi da BOZZA"})
    
    # Override Save.
    def save(self, *args, **kwargs):
        # TODO : Dovrei controllare se il campo impobibile o le IVE (detraibile o no sono cambiate) prima di fare questo
        #        conto in aggiornamento.
        # Calcola l'IVA potenzialmente detraibile e quella comunque indetraibile.
        self.iva_comunque_indetraibile = self.imponibile * self.aliquota_IVA * self.percentuale_IVA_indetraibile / 10000
        self.iva_potenzialmente_detraibile = self.imponibile * self.aliquota_IVA / 100 - self.iva_comunque_indetraibile
        self.dirty = True
        super().save(*args, **kwargs)
        
        # Se ci sono già delle ripartizioni le aggiorna con i nuovi valori.
        # TODO : Anche questo lo dovrei fare solo se ho aggiornato qualche cosa che tocca questi campi. Da vedere dopo.
        _aggiorna_ripartizioni_se_presenti(self.pk, ACQUISTO_WEB)
    
    def calcola_costo_totale(self):
        self.dirty, self.costo, self.cdc_verbose = _calcola_costo_totale(self.pk, ACQUISTO_WEB)
        self.save()
    
    def aggiorna_ripartizioni(self):
        ripartizioni = RipartizioneSpesaPerCDC.objects.filter(acquisto=self.id)
        for ripartizione in ripartizioni:
            ripartizione.save(force_update=True)


"""
class Spesa(SiwGeneralModel):
    # Definizione degli stati
    STATO_BOZZA = 0
    STATO_DA_AUTORIZZARE = 10
    STATO_AUTORIZZATO = 20
    STATO_INVIATO = 30
    STATO_EVASO = 40
    STATO_CONFORME = 50
    STATO_LIQUIDATO = 60
    STATO_CHIUSO = 1000
    STATO_ANNULLATO = 900
    STATO_SPESA_CHOICES = (
        (STATO_BOZZA, 'Bozza'),
        (STATO_DA_AUTORIZZARE, 'Da Autorizzare'),
        (STATO_AUTORIZZATO, 'Autorizzato'),
        (STATO_INVIATO, 'Inviato'),
        (STATO_EVASO, 'Evaso'),
        (STATO_CONFORME, 'Conforme'),
        (STATO_LIQUIDATO, 'Liquidato'),
        (STATO_CHIUSO, 'Chiuso'),
        (STATO_ANNULLATO, 'ANNULLATO'),
    )
    
    # Definizione del tipo di acquisto
    # Se l'intero è < 100 ho tipo 1, se compreso tra 100 e 300 ho tipo 2, altrimenti ho tipo 3
    TIPO_ACQUISTO_CON_ORDINE_A_FORNITORE = 10
    TIPO_ACQUISTO_WEB = 110
    TIPO_ACQUISTO_SENZA_ORDINE = 120
    TIPO_SPESE_DI_CASSA = 130
    TIPO_SPESE_CON_PREPAGATA = 140
    TIPO_SPESE_CON_VISA = 150
    TIPO_NOTE_SPESE = 160
    TIPO_CARTA_CARBURANTE = 170
    TIPO_SPESA_CHOICES = (
        (TIPO_ACQUISTO_CON_ORDINE_A_FORNITORE, 'Acquisto con Ordine a Fornitore'),
        (TIPO_ACQUISTO_WEB, 'Acquisto Web'),
        (TIPO_ACQUISTO_SENZA_ORDINE, 'Acquisto senza ordine'),
        (TIPO_SPESE_DI_CASSA, 'Spese di cassa'),
        (TIPO_SPESE_CON_PREPAGATA, 'Spese con Prepagata'),
        (TIPO_SPESE_CON_VISA, 'Spese con visa'),
        (TIPO_NOTE_SPESE, 'Note Spese'),
        (TIPO_CARTA_CARBURANTE, 'Carta Carburante')
    )
    
    anno_formativo = models.ForeignKey(AnnoFormativo, on_delete=models.PROTECT)
    numero_protocollo = models.CharField(max_length=10)
    data_ordine = models.DateField()
    
    stato = models.IntegerField(choices=STATO_SPESA_CHOICES, default=STATO_BOZZA)
    tipo = models.IntegerField(choices=TIPO_SPESA_CHOICES)
    
    # Descrizione e fornitore
    fornitore = models.ForeignKey(Fornitore, on_delete=models.PROTECT, null=True)
    descrizione = models.TextField()
    
    # Costo acquisto in funzione dei cdc cui si riferisce.
    imponibile = models.DecimalField(max_digits=7, decimal_places=2)
    aliquota_IVA = models.DecimalField(max_digits=4, decimal_places=2)
    percentuale_IVA_indetraibile = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    costo = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    
    protocollo_fattura_fornitore = models.CharField(max_length=10, blank=True)
    
    note = models.TextField(blank=True)
    conforme = models.BooleanField(default=False)
    
    # Campi di sistema per garantire che le voci ordini vengano completate.
    dirty = models.BooleanField(default=True)
    iva_comunque_indetraibile = models.DecimalField(max_digits=7, decimal_places=2)
    iva_potenzialmente_detraibile = models.DecimalField(max_digits=7, decimal_places=2)
    cdc_verbose = models.CharField(null=True, max_length=50)
    
    class Meta:
        verbose_name = "Spesa"
        verbose_name_plural = "Spese"
    
    def __str__(self):
        return self.descrizione
    
    # Override Save.
    def save(self, *args, **kwargs):
        # TODO : Dovrei controllare se il campo impobibile o le IVE (detraibile o no sono cambiate) prima di fare questo
        #        conto in aggiornamento.
        # Calcola l'IVA potenzialmente detraibile e quella comunque indetraibile.
        self.iva_comunque_indetraibile = self.imponibile * self.aliquota_IVA * self.percentuale_IVA_indetraibile / 10000
        self.iva_potenzialmente_detraibile = self.imponibile * self.aliquota_IVA / 100 - self.iva_comunque_indetraibile
        self.dirty = True
        self.controlla_fornitore_se_necessario()
        self.impone_descrizione_se_necessario()
        super().save(*args, **kwargs)
        
        # Se ci sono già delle ripartizioni le aggiorna con i nuovi valori.
        # TODO : Anche questo lo dovrei fare solo se ho aggiornato qualche cosa che tocca questi campi. Da vedere dopo.
        self._aggiorna_ripartizioni_se_presenti(self.pk)
    
    @staticmethod
    def _aggiorna_ripartizioni_se_presenti(pk):
        ripartizioni = RipartizioneSpesaPerCDC.objects.filter(spesa=pk)
        for ripartizione in ripartizioni:
            ripartizione.save()
    
    def calcola_costo_totale(self):
        # Controllo che le percentuali delle ripartizioni facciano 100 altrimenti esco con falso.
        percentuali = RipartizioneSpesaPerCDC.objects.filter(spesa=self.pk)
        percentuali = percentuali.only('percentuale_di_competenza')
        percentuali = percentuali.aggregate(Sum('percentuale_di_competenza'))
        valore = percentuali['percentuale_di_competenza__sum'] if percentuali['percentuale_di_competenza__sum'] else 0
        if valore != 100:
            return False
        # Sommo i costi delle ripartizioni per fare il conto di quanto costa la singola spesa
        ripartizioni = RipartizioneSpesaPerCDC.objects.filter(spesa=self.pk)
        ripartizioni = ripartizioni.aggregate(Sum('costo_totale'))
        self.costo = ripartizioni['costo_totale__sum']
        # Infine compilo la stringa dei centri di costo.
        ripartizioni = RipartizioneSpesaPerCDC.objects.filter(spesa=self.pk)
        linea = ''
        for ripartizione in ripartizioni:
            token = str(ripartizione.percentuale_di_competenza) + '% ' + ripartizione.cdc.nome
            linea = linea + ', ' + token if linea else token
        self.cdc_verbose = linea
        self.dirty = False
        self.save()
    
    def controlla_fornitore_se_necessario(self):
        if self.tipo < 100 and self.fornitore is None:
            raise ValidationError({'fornitore': "Per questo tipo di spesa il Fornitore è obbligatorio !"})
    
    def impone_descrizione_se_necessario(self):
        if 100 < self.tipo < 300:
            self.descrizione = self.get_tipo_display()
"""


class RipartizioneSpesaPerCDC(SiwGeneralModel):
    acquisto = models.ForeignKey(AcquistoConOrdine, on_delete=models.PROTECT)
    cdc = models.ForeignKey(CentroDiCosto, on_delete=models.PROTECT)
    percentuale_di_competenza = models.DecimalField(max_digits=5, decimal_places=2)
    costo_totale = models.DecimalField(max_digits=7, decimal_places=2)
    
    class Meta:
        verbose_name = "Ripartizione Costo su CDC"
        verbose_name_plural = "Ripartizione Costo su CDC"
    
    def __str__(self):
        return 'Quotaparte di ' + self.acquisto.descrizione + ' su ' + self.cdc.descrizione

    def clean(self):
        # Il valore della singola ripartizione non può eccedere il 100% o essere minore di 1%
        if hasattr(self, 'percentuale_di_competenza'):
            if int(self.percentuale_di_competenza) > 100:
                raise ValidationError(
                    {'percentuale_di_competenza': "La percentuale di competenza non può eccedere il 100%"})
            # Il valore delle singola ripartizione non può essere 0 o negativo
            if int(self.percentuale_di_competenza) <= 0:
                raise ValidationError(
                    {'percentuale_di_competenza': "La percentuale di competenza non può essere minore di 1%"})
        
        # La somma di tutte le percentuali di tutte le ripartizioni non può eccedere il 100%.
        # Se non ho un acquisto di riferimento non posso fare il controllo.
        if hasattr(self, 'acquisto'):
            if self._verifica_se_percentuali_eccedute(self.acquisto, self.percentuale_di_competenza, self.pk):
                raise ValidationError({'percentuale_di_competenza': "La somma di tutte le percentuali "
                                                                    "per questo acquisto eccede il 100%"})

    # Override Save.
    # Calcola il costo totale della voce di ordine in funzione della detraibilità del singolo cdc
    def save(self, *args, **kwargs):
        # Calcola il costo della ripartizione.
        base_imponibile = self.acquisto.imponibile + self.acquisto.iva_comunque_indetraibile
        if not self.cdc.iva_detraibile:
            base_imponibile += self.acquisto.iva_potenzialmente_detraibile
        self.costo_totale = base_imponibile * self.percentuale_di_competenza / 100
        super().save(*args, **kwargs)

    @staticmethod
    def _verifica_se_percentuali_eccedute(acquisto, percentuale, pk):
        percentuali = RipartizioneSpesaPerCDC.objects.filter(acquisto=acquisto)
        if pk:
            percentuali = percentuali.exclude(pk=pk)
        percentuali = percentuali.only('percentuale_di_competenza')
        percentuali = percentuali.aggregate(Sum('percentuale_di_competenza'))
        valore = percentuali['percentuale_di_competenza__sum'] if percentuali['percentuale_di_competenza__sum'] else 0
        return True if valore + percentuale > 100 else False

