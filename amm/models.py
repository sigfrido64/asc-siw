# coding=utf-8
from django.db import models
from django.core.validators import MinLengthValidator

from siw.siwmodels import SiwGeneralModel
from collaboratori.models import Collaboratore
from anagrafe.models import PersonaInAzienda


__author__ = "Pilone Ing. Sigfrido"


class IncarichiExtension(models.Model):
    """
            Campi per la gestione di sistema.
    """
    # Data da cui parto a considerare valido il record.
    valido_dal = models.DateField(verbose_name="Data di inizio validità")
    # Data in cui il record cessa di essere valido.
    valido_al = models.DateField(verbose_name="Data di fine validità")

    class Meta:
        abstract = True

    def incaricabile(self, data_inizio_incarico, data_fine_incarico):
        raise NotImplementedError("La classe deve definire questo metodo !")

    def costo_azienda(self, lista_pagamenti):
        raise NotImplementedError("La classe deve definire questo metodo !")


class CentroDiCosto(SiwGeneralModel):
    """
    Definizione dei centri di costo.
    TODO

    Le date di inizio e fine validità devono stare entro quelle della radice. Possono essere minori ma non maggiori.
    Di default posso proporre quelle nella vista della creazione quando ci sarà.

    Se ho un'iniziativa root deve chiamarsi AF AAAA-AAAA con i due anni consecutivi.
    Se non è root questa nomenclatura non deve essere possibile.

    Se ho iva indetraibile tutte le sotto iniziative devono essere dello stesso tipo.

    Nella vista di creazione le root devono essere solo quelle con root abilitato invece nei parent ci possono essere
    solo quelli sotto la root scelta sopra.

    Le root devono essere uniche per evitare casino con i nomi mentre sotto di loro le iniziative possono anche avere
    lo stesso nome per replicare la struttura. Questo permette, se serve, si avere la stessa iniziativa a cavallo di
    diversi anni formativi. Sarebbe meglio un controllo per evitare le repliche non volute per cui mi chiede se è la
    stessa e se non lo è non mi lascia usare lo stesso nome.

    Il controllo treeview permette di aggiungere elementi in modo semplice sotto un certo nodo ?
    """
    # Riferimenti al parent ed alla radice e se lui stesso è una radice.
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT,
                               related_name='iniziativa_parent')
    root = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT,
                             related_name='iniziativa_root')
    is_root = models.BooleanField(default=False)
    # Dati dell'iniziativa.
    nome = models.CharField(max_length=30, validators=[MinLengthValidator(3)],
                            verbose_name="Nome sintetico dell'iniziativa")
    descrizione = models.CharField(
        max_length=120, validators=[MinLengthValidator(5)], verbose_name="Breve descrizione dell'iniziativa")
    
    cup = models.CharField(max_length=30, blank=True, verbose_name='CUP se presente')
    cig = models.CharField(max_length=30, blank=True, verbose_name='CIG se presente')
    iva_detraibile = models.BooleanField(
        default=True, verbose_name="L'IVA delle spese connesse all'iniziativa è scaricabile ?")
    
    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    # Data da cui parto a considerare valido il record.
    valido_dal = models.DateField(verbose_name="Data di inizio validità")
    # Data in cui il record cessa di essere valido.
    valido_al = models.DateField(verbose_name="Data di fine validità")
    # Data di aggiornamento del record.

    # META Class.
    class Meta:
        verbose_name = "Centro di Costo"
        verbose_name_plural = "Centri di Costo"
        ordering = ['nome']

    # To String.
    def __str__(self):
        root = self.root.nome if self.root else '^'
        return root + ' > ' + self.nome + ' - ' + self.descrizione

    # Custon Check fields.
    # TODO qui è da decidere cosa devo contrallare quando devo salvare un centro di costo.
    def clean(self):
        pass


class Occasionale(SiwGeneralModel, IncarichiExtension):
    """
    Definizione degli elementi amministrativi per i collaboratori occasionali.
    """
    collaboratore = models.OneToOneField(Collaboratore, on_delete=models.PROTECT)
    documenti_consegnati = models.BooleanField(default=False)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    class Meta:
        verbose_name = "Collaborazione Occasionale"
        verbose_name_plural = "Collaborazioni Occasionali"

    def incaricabile(self, data_inizio_incarico, data_fine_incarico):
        """
        devo dire se il collaboratore 
        :param data_inizio_incarico:
        :param data_fine_incarico:
        :return:

        Dopo che ha consegnato documenti e se non ha cubato più di 5.000 euro nell'anno solare (tra tutti i
        committenti cosa che non posso controllare ma che l'amministrazione chiede.)
        Quindi dovrei avere una scheda per anno ed eventualmente ridurre il montante in funzione di altre collaborazioni
        """
        raise NotImplementedError("La classe deve definire questo metodo !")

    def costo_azienda(self, lista_pagamenti):
        raise NotImplementedError("La classe deve definire questo metodo !")

    def __str__(self):
        return self.collaboratore.persona.cognome + ' - ' + self.collaboratore.persona.nome


class Parasubordinato(SiwGeneralModel, IncarichiExtension):
    """
    Definizione degli elementi amministrativi per i collaboratori occasionali.
    """
    collaboratore = models.ForeignKey(Collaboratore, on_delete=models.PROTECT)
    documenti_consegnati = models.BooleanField(default=False)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    class Meta:
        verbose_name = "Collaborazione CoCoCo"
        verbose_name_plural = "Collaborazioni CoCoCo"

    def incaricabile(self, data_inizio_incarico, data_fine_incarico):
        """
        devo dire se il collaboratore
        :param data_inizio_incarico:
        :param data_fine_incarico:
        :return:
        Devo avere una matricola denunciata sul GECO e le date di inizio e fine della matricola stessa. Entro queste date
        posso caricare incarichi, al di fuori no.
        """
        raise NotImplementedError("La classe deve definire questo metodo !")

    def costo_azienda(self, lista_pagamenti):
        """
        Al momento ho due casi :
        1) Dipendenti e Pensionati
        2) Disoccupati

        :param lista_pagamenti:
        :return:
        """
        raise NotImplementedError("La classe deve definire questo metodo !")

    def __str__(self):
        return self.collaboratore.persona.cognome + ' - ' + self.collaboratore.persona.nome


class Autonomo(SiwGeneralModel, IncarichiExtension):
    """
    Definizione degli elementi amministrativi per i collaboratori autonomi.

    TODO
    I collaboratori autonomi possono essere solo persone fisiche che siano titolari di ditta individuale altrimenti
    si ricade nel caso di azienda e quindi di possibile delega e quindi da valutare con attenzione !
    
    """
    collaboratore = models.ForeignKey(Collaboratore, on_delete=models.PROTECT)
    personainazienda = models.ForeignKey(PersonaInAzienda, on_delete=models.PROTECT)
    documenti_consegnati = models.BooleanField(default=False)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')

    class Meta:
        verbose_name = "Collaborazione Autonoma"
        verbose_name_plural = "Collaborazioni Autonome"

    def incaricabile(self, data_inizio_incarico, data_fine_incarico):
        """
        devo dire se il collaboratore
        :param data_inizio_incarico:
        :param data_fine_incarico:
        :return:
        Incaricabile anche da subito. Basta che consegni i documenti.
        """
        raise NotImplementedError("La classe deve definire questo metodo !")

    def costo_azienda(self, lista_pagamenti):
        raise NotImplementedError("La classe deve definire questo metodo !")

    def __str__(self):
        return self.collaboratore.persona.cognome + ' - ' + self.collaboratore.persona.nome


class IncaricoDocenza(SiwGeneralModel):
    from corsi.models import Corso

    numero = models.IntegerField()

    data_incarico = models.DateField(auto_now=True)
    data_inizio_incarico = models.DateField(auto_now=True)
    data_termine_incarico = models.DateField(auto_now=True)

    collaboratore = models.ForeignKey(Collaboratore, on_delete=models.PROTECT)
    tipologia_collaboratore = models.IntegerField()

    corso = models.ForeignKey(Corso, on_delete=models.PROTECT)

    materia = models.CharField(max_length=80)

    ore_previste = models.FloatField()
    parametro_orario = models.FloatField()
    aggiuntivo_corso = models.FloatField()

    importo_incarico_previsto = models.FloatField()
    importo_incarico_effettivo = models.FloatField()

    costo_incarico_previsto = models.FloatField()
    costo_incarico_effettivo = models.FloatField()

    cdc = models.ForeignKey(CentroDiCosto, on_delete=models.PROTECT)

    note = models.TextField(blank=True, default='', verbose_name='Eventuali note')


class RilevamentoDocenza(SiwGeneralModel):
    incarico_docenza = models.ForeignKey(IncaricoDocenza, on_delete=models.PROTECT)
    ore_rilevate = models.IntegerField()
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


"""
class IncaricoDocenza(SiwGeneralModel):
    DOCENZA = 'D'
    ATTIVITA_VARIE = 'V'
    INCARICO_CHOICES = (
        (DOCENZA, 'Docenza'),
        (ATTIVITA_VARIE, 'Attività Varie diverse dalla Docenza'),
    )
    tipologia = models.CharField(max_length=1, choices=INCARICO_CHOICES, default=DOCENZA)
    numero = models.IntegerField()
    data_incarico = models.DateField(auto_now=True)
    data_inizio_incarico = models.DateField(auto_now=True)
    data_termine_incarico = models.DateField(auto_now=True)
    collaboratore = models.ForeignKey(Collaboratore, on_delete=models.PROTECT)

"""