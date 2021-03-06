# coding=utf-8
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

from siw.siwmodels import SiwGeneralModel

__author__ = "Pilone Ing. Sigfrido"


class CentroDiCosto(SiwGeneralModel):
    """
    Definizione dei centri di costo.
    TODO

    devo prevedere una rappresentazione "umana" anche in interfaccia admin altrimenti mi posso scordare aiuto da
    chiunque.

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
    """
        Riferimenti al parent ed alla radice e se lui stesso è una radice.
        root : Mi serve per semplificare la ricerca di tutte le iniziative di un anno formativo, altrimenti dovrei
            scorrere tutto l'albero ogni volta !
    """
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
        # parent = self.parent
        # root = ''
        # while parent:
        #    root = parent.nome + '->' + root
        #    parent = parent.parent
        # return root + self.nome + ' : ' + self.descrizione
        return self.nome

    # Custon Check fields.
    def clean(self):
        # Se non è root il campo 'parent' deve essere valorizzato.
        if not self.is_root and self.parent is None:
            raise ValidationError("Non è stato indicato un cdc padre !")
        
        # La data di inizio validità deve essere minore della data di fine validità.
        if hasattr(self, 'valido_al') and hasattr(self, 'valido_dal'):
            if self.valido_al and self.valido_dal:
                if self.valido_al <= self.valido_dal:
                    raise ValidationError({'valido_dal': "Non può essere successivo all'inizio validità"},
                                          {'valido_al': "Non può essere precedente la fine di validità"})


"""
class AnaliticoCostiRicavi(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT,
                               related_name='iniziativa_parent')
    nome = models.CharField(max_length=30, validators=[MinLengthValidator(3)],
                            verbose_name="Nome sintetico dell'iniziativa")
    descrizione = models.CharField(
        max_length=120, validators=[MinLengthValidator(5)], verbose_name="Breve descrizione dell'iniziativa")
    costo = models.BigIntegerField(default=0)
    ricavo = models.BigIntegerField(default=0)
    budget_costo = models.BigIntegerField(default=0)
    budget_ricavo = models.BigIntegerField(default=0)
"""