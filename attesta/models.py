# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.db import models
from operator import itemgetter

# Create your models here.


class Report(models.Model):
    """
    Modello che definisce i report che sono in grado di produrre
    """
    # DATABASE FIELDS
    nome = models.CharField(max_length=30, primary_key=True)
    descrizione = models.CharField(max_length=80, blank=False)
    nome_file = models.CharField(max_length=80, blank=False)
    subfolder = models.CharField(max_length=80, blank=True, default='')
    downloadfilename = models.CharField(max_length=80, blank=False)
    note = models.TextField(blank=True)
    
    # META CLASS
    class Meta:
        verbose_name = 'report'
        verbose_name_plural = 'reports'

    # TO STRING METHOD
    def __str__(self):
        return self.nome


class ReportAssociato(models.Model):
    """
    Modello che definisce i report associati ad ogni specifico corso.
    """
    # DATABASE FIELDS
    corso = models.CharField(max_length=10, primary_key=True)
    reports = models.TextField('Lista dei report associati al corso', blank=True)
    
    # META CLASS
    class Meta:
        verbose_name = 'report associato'
        verbose_name_plural = 'report associati'
    
    # TO STRING METHOD
    def __str__(self):
        return self.corso

    @staticmethod
    def lista_report_associati(corso):
        """
        Riporta la lista dei report associati ad un dato corso per comporre l'option del select HTML.
        
        :param corso: Il corso di cui voglio la lista dei report associati.
        :return: Lista dei report associati a quel corso con nome e descrizione da mostrare nelle option.
        """
        # Recupera la lista dei report associati ad un corso.
        reports = ReportAssociato.objects.filter(corso=corso).first()
        lista = []
        # Itera su ogni report per prendere la descrizione dal record dei report.
        if reports:
            lista_reports = eval(reports.reports)
            for report in lista_reports:
                # Per ogni elemento fa un dizionario con le chiavi 'nome' e 'descrizione'
                report = list(Report.objects.filter(nome=report).values('nome', 'descrizione'))
                if report:
                    # Allunga la lista dei dizionari.
                    lista += report
            # Adesso ordina la lista in base alla descrizione
            lista.sort(key=itemgetter('descrizione'))
        return lista
