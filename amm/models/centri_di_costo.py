# coding=utf-8
from django.db import models
from django.core.validators import MinLengthValidator

from siw.siwmodels import SiwGeneralModel
from collaboratori.models import Collaboratore
from anagrafe.models import PersonaInAzienda


__author__ = "Pilone Ing. Sigfrido"


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