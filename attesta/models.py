from django.db import models

# Create your models here.


class Report(models.Model):
    """
    Modello che definisce i report che sono in grado di produrre
    """
    # DATABASE FIELDS
    nome = models.CharField(max_length=30, primary_key=True)
    descrizione = models.CharField(max_length=80)
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
        verbose_name = 'report'
        verbose_name_plural = 'reports'
    
    # TO STRING METHOD
    def __str__(self):
        return self.corso
