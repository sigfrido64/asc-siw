# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class SiwPermessi(object):
    """
    Helper Class per la definizione dei Permessi in modo centrale ed univoco.
    Ogni nome di permesso DEVE iniziare con una maiuscola per essere poi compreso come tale nella funzione che lo
    trasforma in dizionario.
    """
    STAMPE_MDL = 'stampe_mdl'

    """
    Sezione Amministrazione
    """
    AMM_CDC_READ = 'amm_cdc_read'

    """
    Collaboratori
    """
    COLLABORATORI_LISTA_READ = 'coll_lista_view'
    COLLABORATORE_MOSTRA = 'coll_mostra_view'

    """
    Sezione Menù. Al momento uso un permesso per mostrare o meno le voci di menù così che sia possibile avere
    accesso ad una pagina anche se non ho il menù visualizzato in quanto i permessi saranno diversi.
    TODO : Da verificare se questa impostazione può o meno funzionare in generale e se non crea più problemi di quanti
    ne risolve nel mismatch tra permessi sulle viste e permessi per i menù
    """
    MENU_AMM = 'menu_amm'
    MENU_AMM_CDC = 'menu_cdc'

    @staticmethod
    def as_dict():
        # Trasforma in dizionario dei permessi tutte le variabili nella radice della Classe se iniziano con una
        # maiuscola.
        const = dict()
        for key, value in SiwPermessi.__dict__.items():
            if key[0].isupper():
                const[key] = value
        return const


class SiwRuoli(object):
    """
    Helper Classe per la definizione dei Ruoli in modo centrale ed univoco.
    """
    MDL = {SiwPermessi.STAMPE_MDL}
    AMM = {SiwPermessi.AMM_CDC_READ, SiwPermessi.MENU_AMM, SiwPermessi.MENU_AMM_CDC}
    COLL = {SiwPermessi.COLLABORATORI_LISTA_READ, SiwPermessi.COLLABORATORE_MOSTRA}
    

class Profile(models.Model):
    """
    Estende il modello dell'Utente di Sistema andando ad aggiungere i peressi ed i ruoli per la protezioe dei dati.
    ATTENZIONE : I permessi negati prevalgono su quelli concessi !
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Legame al record dell'Utente
    ruoli = models.TextField(default=False, help_text="Lista dei ruoli che spettano all'utente",
                             verbose_name="Ruoli assegnati all'utente")
    permessi = models.TextField(default=False, help_text="Lista dei permessi concessi all'utente",
                                verbose_name="Permessi Concessi", blank=True)
    negati = models.TextField(default=False, help_text="Lista dei permessi esplicitamente negati all'utente",
                              verbose_name="Permessi Esplicitamente negati", blank=True)
    tmp_permessi = models.TextField(default=False, help_text="Dizionario dei permessi temporaneamente concessi con "
                                    "timestamp di termine validità", verbose_name="Permessi temporaneamente "
                                    "concessi", blank=True)
    tmp_negati = models.TextField(default=False, help_text="Dizionario dei permessi temporaneamente negati con "
                                  "timestamp di termine validità", verbose_name="Permessi temporaneamente "
                                  "negati", blank=True)
    must_change_password = models.BooleanField(default=False, help_text="Se True l'utente deve cambiare la password "
                                               "al primo accesso")

    # META CLASS
    class Meta:
        verbose_name = 'profilo'
        verbose_name_plural = 'profili'
        
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

"""
TODO : Da rivedere la gestione dell'obbligo di cambio password !
@receiver(pre_save, sender=User)
def password_change_signal(sender, instance, **kwargs):
    try:
        user = User.objects.get(username=instance.username)
        if not user.password == instance.password:
            instance.profile.must_change_password = False
    except User.DoesNotExist:
        pass
"""


class Ruoli(models.Model):
    """
    Definisco la tabella dei ruoli con la lista dei permessi concessi e negati.
    """
    ruolo = models.CharField(max_length=80, verbose_name="Nome del ruolo", primary_key=True)
    permessi = models.TextField(default=False, help_text="Lista dei permessi concessi al ruolo",
                                verbose_name="Permessi Concessi", blank=True)
    negati = models.TextField(default=False, help_text="Lista dei permessi esplicitamente negati al ruolo",
                              verbose_name="Permessi Esplicitamente negati", blank=True)

    # META CLASS
    class Meta:
        verbose_name = 'ruolo'
        verbose_name_plural = 'ruoli'

    def __str__(self):
        return self.ruolo
    

def update_perms(permessi, straddendum):
    addendum = eval(straddendum)
    nuovo = set()
    nuovo.update(permessi)
    if addendum:
        nuovo.update(addendum)
    return nuovo


def get_real_perms(request_user):
    """
    
    :param request_user: request.user object
    :return: Lista dei permessi reali attribuiti all'utente nel momento della richiesta.
    
    ATTENZIONE : I permessi negati prevalgono rispetto a quelli concessi.
    Uso gli insiemi per cui nel data base devo usare {}
    TODO : Manca la gestione dei permessi temporanei !!!
    """
    # Recupero i dati dell'utente loggato.
    user = User.objects.get(pk=request_user.id)

    # Recupero tutti i permessi associati e negati a quel ruolo. Li recupero prima perchè poi aggiungerò e toglierò
    # gli altri. Così i secondi avranno la precedenza su questi.
    lista_ruoli = eval(user.profile.ruoli)
    permessi = negati = set()
    if lista_ruoli:
        for ruolo in lista_ruoli:
            system_role = Ruoli.objects.get(pk=ruolo)
            permessi = update_perms(permessi, system_role.permessi)
            negati = update_perms(negati, system_role.negati)

    # Adesso aggiungo quelli specifici dell'utente.
    permessi = update_perms(permessi, user.profile.permessi)
    negati = update_perms(negati, user.profile.negati)

    # Ora tolgo dai permessi quelli che sono esplicitamente negati.
    permessi.difference_update(negati)
    
    return permessi


def has_permission(user, permission_name):
    """Check if a user has a given permission."""
    # Superuser win all !
    if user and user.is_superuser:
        return True
    # Otherwise check for real permissions.
    return permission_name in user.si_perms
