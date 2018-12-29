# coding=utf-8
from django.db import models
from siw.siwmodels import SiwGeneralModel

"""
--
-- Se la stringa è nulla riporto NULL.
--
IF @Ragione_Sociale IS NULL
    RETURN NULL

--
-- Porto la Ragione Sociale in maiuscolo.
--
SET @V1 = UPPER(@Ragione_Sociale)

--
-- Elimino i segni come . ; , & ' ' - " ( ) / \
--
SET @V1 = REPLACE (@V1, '.', '')
SET @V1 = REPLACE (@V1, ';', '')
SET @V1 = REPLACE (@V1, ',', '')
SET @V1 = REPLACE (@V1, '&', '')
SET @V1 = REPLACE (@V1, '-', '')
SET @V1 = REPLACE (@V1, '"', '')
SET @V1 = REPLACE (@V1, '(', '')
SET @V1 = REPLACE (@V1, ')', '')
SET @V1 = REPLACE (@V1, '/', '')
SET @V1 = REPLACE (@V1, '\', '')
SET @V1 = REPLACE (@V1, ' ', '')

--
-- Riporto il risultato.
--
RETURN @V1
"""


class Persona(SiwGeneralModel):
    """
    Persone : Sono solo persone fisiche.

    Qui vado a memorizzare solo i dati personali. Quindi se poi li trovo definiti in qualche azienda i dati che trovo
    la sono relativi al loro recapito nelle varie aziende.
    """
    # Riferimenti agli altri database.
    # Assocam Anagrafica Persone -> Matricola Assocam
    asc_id = models.BigIntegerField(unique=True, default=None, null=True)
    asc_data_elemento = models.DateTimeField(null=True, blank=True)
    asc_data_aggiornamento = models.DateTimeField(null=True, blank=True)

    asc_ca_id = models.BigIntegerField(unique=True, default=None, null=True)   # Contatto azienda
    asc_ca_data_elemento = models.DateTimeField(null=True, blank=True)
    asc_ca_data_aggiornamento = models.DateTimeField(null=True, blank=True)

    r2k_id = models.BigIntegerField(unique=True, default=None, null=True)      # Matricola rete 2000
    r2k_data_elemento = models.DateTimeField(null=True, blank=True)
    r2k_data_aggiornamento = models.DateTimeField(null=True, blank=True)

    # Nome
    titolo = models.CharField(max_length=20, blank=True)
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    vip = models.BooleanField(default=False)

    # Luogo e data di nascita
    comune_nascita = models.CharField(max_length=50, blank=True)
    provincia_nascita = models.CharField(max_length=2, blank=True)
    stato_nascita = models.CharField(max_length=40, blank=True)
    data_nascita = models.DateField(null=True, blank=True)

    # Cittadinanza.
    cittadinanza = models.CharField(max_length=40, blank=True)

    # Sesso
    sesso = models.CharField(max_length=1)

    # Domicilio
    indirizzo_domicilio = models.CharField(max_length=50, blank=True)
    comune_domicilio = models.CharField(max_length=50, blank=True)
    cap_domicilio = models.CharField(max_length=5, blank=True)
    provincia_domicilio = models.CharField(max_length=2, blank=True)
    regione_domicilio = models.CharField(max_length=25, blank=True)
    stato_domicilio = models.CharField(max_length=25, blank=True)

    # Residenza
    indirizzo_residenza = models.CharField(max_length=50, blank=True)
    comune_residenza = models.CharField(max_length=50, blank=True)
    cap_residenza = models.CharField(max_length=5, blank=True)
    provincia_residenza = models.CharField(max_length=2, blank=True)
    regione_residenza = models.CharField(max_length=25, blank=True)
    stato_residenza = models.CharField(max_length=25, blank=True)

    # Codice Fiscale
    cf = models.CharField(max_length=16, blank=True)

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
        verbose_name = "Persona"
        verbose_name_plural = "Persone"
        ordering = ['cognome']

    # To String.
    def __str__(self):
        return self.cognome + ' - ' + self.nome


class Azienda(SiwGeneralModel):
    """
    Aziende : Anagrafica Aziende.

    """
    # Riferimenti agli altri database.
    # Assocam Anagrafica Aziende -> Matricola Assocam
    asc_id = models.BigIntegerField(unique=True, default=None, null=True)
    asc_data_elemento = models.DateTimeField(null=True, blank=True)
    asc_data_aggiornamento = models.DateTimeField(null=True, blank=True)

    r2k_id = models.BigIntegerField(unique=True, default=None, null=True)      # Matricola rete 2000
    r2k_data_elemento = models.DateTimeField(null=True, blank=True)
    r2k_data_aggiornamento = models.DateTimeField(null=True, blank=True)

    # Ragione sociale e descrizione azienda.
    ragione_sociale = models.CharField(max_length=100)
    descrizione = models.CharField(max_length=200, blank=True)

    # Indirizzo
    indirizzo = models.CharField(max_length=50, blank=True)
    comune = models.CharField(max_length=50, blank=True)
    cap = models.CharField(max_length=5, blank=True)
    provincia = models.CharField(max_length=2, blank=True)
    regione = models.CharField(max_length=25, blank=True)
    stato = models.CharField(max_length=25, blank=True)

    # Dati Amministrativi
    cf = models.CharField(max_length=16, verbose_name="Codice Fiscale")
    piva = models.CharField(max_length=16, verbose_name="Partita Iva")

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

    # Sito Web
    sito_web = models.CharField(max_length=50, blank=True)
    hashragionesociale = models.CharField(max_length=100)

    # Privacy
    accetta_promozioni = models.BooleanField(default=True)

    # Campo note
    note = models.TextField(blank=True, verbose_name='Eventuali note')

    # META Class.
    class Meta:
        verbose_name = "Azienda"
        verbose_name_plural = "Aziende"
        ordering = ['ragione_sociale']

    # To String.
    def __str__(self):
        return self.ragione_sociale


class PersonaInAzienda(SiwGeneralModel):
    # Riferimenti alla persona ed all'Azienda.
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)
    azienda = models.ForeignKey(Azienda, on_delete=models.PROTECT)

    # Posizione occupata in Azienda.
    posizione = models.CharField(max_length=50, blank=True)

    # Recapiti telefonici Aziendali
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
        verbose_name = "Membro Azienda"
        verbose_name_plural = "Membri Aziende"

    # To String.
    def __str__(self):
        return self.persona.cognome + ' , ' + self.persona.nome + ' - ' + self.azienda.ragione_sociale


class TipoTelefonoPersone(models.Model):
    descrizione_telefono = models.CharField(max_length=20)

    # META Class.
    class Meta:
        verbose_name = "Tipo Telefono"
        verbose_name_plural = "Tipi Telefono"

    # To String.
    def __str__(self):
        return self.descrizione_telefono


class TipoMailPersone(models.Model):
    descrizione_mail = models.CharField(max_length=20)

    # META Class.
    class Meta:
        verbose_name = "Tipo Mail"
        verbose_name_plural = "Tipi Mail"

    # To String.
    def __str__(self):
        return self.descrizione_mail


class Fornitore(SiwGeneralModel):
    """
    Fornitore : Anagrafica Fornitori.

    """
    azienda = models.ForeignKey(Azienda, on_delete=models.PROTECT)
    
    # META Class.
    class Meta:
        verbose_name = "Fornitore"
        verbose_name_plural = "Fornitori"

    def __str__(self):
        return self.azienda.ragione_sociale