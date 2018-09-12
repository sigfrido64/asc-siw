# coding=utf-8
from django.db import models
from django.core.exceptions import ValidationError
from anagrafe.models import Persona
from siw.siwmodels import SiwGeneralModel

# Create your models here.


class Dipendente(SiwGeneralModel):
    """
    Dipendenti della Scuola.
    """
    # Anagrafica
    titolo = models.CharField(max_length=20)
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)

    # Luogo e data di nascita
    comune_nascita = models.CharField(max_length=50)
    provincia_nascita = models.CharField(max_length=2)
    stato_nascita = models.CharField(max_length=40)
    data_nascita = models.DateField(null=True)

    # Cittadinanza.
    cittadinanza = models.CharField(max_length=40)

    # Sesso
    sesso = models.CharField(max_length=1)

    # Domicilio
    indirizzo_domicilio = models.CharField(max_length=50)
    comune_domicilio = models.CharField(max_length=50)
    cap_domicilio = models.CharField(max_length=5)
    provincia_domicilio = models.CharField(max_length=2)
    stato_domicilio = models.CharField(max_length=25)

    # Residenza
    indirizzo_residenza = models.CharField(max_length=50)
    comune_residenza = models.CharField(max_length=50)
    cap_residenza = models.CharField(max_length=5)
    provincia_residenza = models.CharField(max_length=2)
    stato_residenza = models.CharField(max_length=25)

    # Codice Fiscale
    cf = models.CharField(max_length=16, unique=True)

    # Recapiti telefonici
    tel1 = models.CharField(max_length=30)
    tel2 = models.CharField(max_length=30, blank=True)
    tel3 = models.CharField(max_length=30, blank=True)
    tel4 = models.CharField(max_length=30, blank=True)
    doc_tel1 = models.CharField(max_length=20)
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

    # Campi relativi all'inizio ed alla fine del rapporto di lavoro.
    data_inizio_collaborazione = models.DateField()
    data_fine_collaborazione = models.DateField(null=True, default=None, blank=True)

    # META Class.
    class Meta:
        verbose_name = "Dipendente"
        verbose_name_plural = "Dipendenti"
        ordering = ['cognome']

    # To String.
    def __str__(self):
        return self.cognome + ' - ' + self.nome


class Collaboratore(SiwGeneralModel):
    """
    Sono le schede dei vari collaboratori della Scuola.

    Qui vado a memorizzare solo i dati che posso usare per contattarli quando sono collaboratori della Scuola.
    """
    persona = models.OneToOneField(Persona, on_delete=models.PROTECT, default=None, null=True)
    dipendente = models.OneToOneField(Dipendente, on_delete=models.PROTECT, default=None, null=True)

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

    # META Class.
    class Meta:
        verbose_name = "Collaboratore"
        verbose_name_plural = "Collaboratori"

    # To String.
    def __str__(self):
        return self.persona.cognome + ' - ' + self.persona.nome \
            if self.persona.cognome else self.dipendente.cognome + ' - ' + self.dipendente.nome

    # Custon Check fields.
    def clean(self):
        # Devo avere almeno un telefono ed una mail per anagrafare un collaboratore.
        telefoni = self.tel1 + self.tel2 + self.tel3 + self.tel4
        mail = self.mail1 + self.mail2
        if not telefoni or not mail:
            raise ValidationError("Devono essere forniti almeno un numero di telefono ed una mail !")

        # Se ho un campo telefono devo aver definito il relativo tipo.
        if self.tel1 and not self.doc_tel1:
            raise ValidationError({'doc_tel1': 'Il tipo di telefono non è stato definito.'})
        if self.tel2 and not self.doc_tel2:
            raise ValidationError({'doc_tel2': 'Il tipo di telefono non è stato definito.'})
        if self.tel3 and not self.doc_tel3:
            raise ValidationError({'doc_tel3': 'Il tipo di telefono non è stato definito.'})
        if self.tel4 and not self.doc_tel1:
            raise ValidationError({'doc_tel4': 'Il tipo di telefono non è stato definito.'})

        # Se ho un campo mail devo aver definito il relativo tipo.
        if self.mail1 and not self.doc_mail1:
            raise ValidationError({'doc_mail1': 'Il tipo di mail non è stato definito.'})
        if self.mail2 and not self.doc_mail2:
            raise ValidationError({'doc_mail2': 'Il tipo di mail non è stato definito.'})

        # Se è un dipendente non devo valorizzare il campo persona e viceversa.
        if self.persona and self.dipendente:
            raise ValidationError('Il collaboratore non può essere contemporaneamente una persona ed un dipendente.')
        # Ma almeno uno dei due deve essere valorizzato.
        if (self.persona or self.dipendente) is None :
            raise ValidationError({'persona': 'Il collaboratore deve essere una persona o un dipendente.',
                                   'dipendente': 'Il collaboratore deve essere una persona o un dipendente.'})
