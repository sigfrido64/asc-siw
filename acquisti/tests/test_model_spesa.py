# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.test import TestCase
from django.core.exceptions import ValidationError
from amm.models.mixins import AnnoFormativo
from amm.models.centri_di_costo import CentroDiCosto
from acquisti.models import AcquistoConOrdine, RipartizioneSpesaPerCDC
from anagrafe.models import Fornitore


class ModelloSpeseTests(TestCase):
    fixtures = ['cdc', 'af', 'azienda', 'fornitore']

    def setUp(self):
        # Recupero i record che mi servono come riferimenti per quello che vado a creare.
        self.anno_formativo = AnnoFormativo.objects.get(anno_formativo='AF 2018-2019')
        self.fornitore = Fornitore.objects.get(pk=1)
        self.cdc1 = CentroDiCosto.objects.get(pk=2)     # Mdl, iva indetraibile
        self.cdc2 = CentroDiCosto.objects.get(pk=10)    # Aziendali, IVA indetraibile
        
        # Carico un acquisto con ordine a fornitore.
        self.spesa = AcquistoConOrdine(anno_formativo=self.anno_formativo, numero_protocollo='123',
                                       data_ordine='1964-11-13', stato=AcquistoConOrdine.STATO_BOZZA,
                                       tipo=AcquistoConOrdine.TIPO_ORDINE_A_FORNITORE,
                                       fornitore=self.fornitore, descrizione='Ordine di Prova',
                                       imponibile=1000, aliquota_IVA=22, percentuale_IVA_indetraibile=20)
        self.spesa.save()
        
    def carica_ripartizione_indetraibile(self):
        self.ripartizione1 = RipartizioneSpesaPerCDC(acquisto=self.spesa, cdc=self.cdc1, percentuale_di_competenza=50)
        self.ripartizione1.save()
        
    def carica_ripartizione_detraibile(self):
        self.ripartizione2 = RipartizioneSpesaPerCDC(acquisto=self.spesa, cdc=self.cdc2, percentuale_di_competenza=50)
        self.ripartizione2.save()
        
    def test_calcoli_iva_detraibile_e_non_su_spesa(self):
        self.assertEqual(self.spesa.iva_comunque_indetraibile, 44)
        self.assertEqual(self.spesa.iva_potenzialmente_detraibile, 176)

    def test_calcolo_corretto_del_costo_di_ripartizione_indetraibile(self):
        self.carica_ripartizione_indetraibile()
        self.assertEqual(self.ripartizione1.costo_totale, 610)

    def test_massima_percentuale_della_singala_ripartizione(self):
        # Poi provo con cdc con IVA indetraibile ma metto percentuale maggiore del 100%.
        ripartizione2 = RipartizioneSpesaPerCDC(acquisto=self.spesa, cdc=self.cdc2, percentuale_di_competenza=160)
        with self.assertRaises(ValidationError):
            ripartizione2.clean()

    def test_massima_percentuale_della_somma_di_tutte_le_ripartizioni(self):
        # Poi provo con cdc con IVA indetraibile ma metto percentuale troppo alta sommata alla prima.
        self.carica_ripartizione_indetraibile()
        ripartizione2 = RipartizioneSpesaPerCDC(acquisto=self.spesa, cdc=self.cdc2, percentuale_di_competenza=60)
        with self.assertRaises(ValidationError):
            ripartizione2.clean()

    def test_calcolo_corretto_del_costo_di_ripartizione_detraibile(self):
        self.carica_ripartizione_detraibile()
        self.assertEqual(self.ripartizione2.costo_totale, 522)

    def test_calcolo_del_costo_totale_della_spesa(self):
        self.carica_ripartizione_indetraibile()
        self.carica_ripartizione_detraibile()
        self.spesa.calcola_costo_totale()
        self.assertEqual(self.spesa.costo, 1132)
        
    def test_percentuale_di_competenza_maggiore_di_zero(self):
        ripartizione = RipartizioneSpesaPerCDC(acquisto=self.spesa, cdc=self.cdc2, percentuale_di_competenza=0)
        with self.assertRaises(ValidationError):
            ripartizione.clean()
