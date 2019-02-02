# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.test import TestCase
from django.core.exceptions import ValidationError
from amm.models.centri_di_costo import CentroDiCosto


class CdcTests(TestCase):
    fixtures = ['cdc', 'af']
    
    def setUp(self):
        # Riferimento a cdc root
        self.cdc_root = CentroDiCosto.objects.get(pk=1)

    def test_no_cdc_senza_padre_se_non_root(self):
        cdc = CentroDiCosto(root=self.cdc_root, nome='Prova', descrizione='Prova', valido_dal='01/01/2019',
                            valido_al='10/01/2019')
        with self.assertRaises(ValidationError):
            cdc.clean()
            
    def test_cdc_senza_padre_ok_se_root(self):
        cdc = CentroDiCosto(root=None, nome='Prova', descrizione='Prova', is_root=True)
        try:
            cdc.clean()
        except ValidationError:
            self.fail("CDC root senza padre non deve dare errore !")
            
    def test_no_cdc_senza_data_inizio_validita(self):
        cdc = CentroDiCosto(root=self.cdc_root, nome='Prova', descrizione='Prova', valido_al='10/01/2019')
        with self.assertRaises(ValidationError):
            cdc.clean()

    def test_no_cdc_senza_data_fine_validita(self):
        cdc = CentroDiCosto(root=self.cdc_root, nome='Prova', descrizione='Prova', valido_dal='01/01/2019')
        with self.assertRaises(ValidationError):
            cdc.clean()

    def test_no_cdc_con_date_inizio_e_fine_uguali(self):
        cdc = CentroDiCosto(root=self.cdc_root, nome='Prova', descrizione='Prova', valido_dal='01/01/2019',
                            valido_al='01/01/2019')
        with self.assertRaises(ValidationError):
            cdc.clean()

    def test_no_cdc_con_date_inizio_e_fine_incoerenti(self):
        cdc = CentroDiCosto(root=self.cdc_root, nome='Prova', descrizione='Prova', valido_dal='10/01/2019',
                            valido_al='01/01/2019')
        with self.assertRaises(ValidationError):
            cdc.clean()
