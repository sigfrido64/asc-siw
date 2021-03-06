# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from accounts.models import get_real_perms, SiwPermessi
from django.core.exceptions import FieldDoesNotExist
from threading import local
from django.conf import settings
from siw.sig_utils import set_anno_formativo_default
import sys


# Crea un'istanza di _user diversa per ogni thread.
# Così aggiungendo un valore il valore sarà diverso per ogni thread e sarà sempre sincronizzato con lui.
_user = local()


def get_current_username():
    # TODO : Attenzione che devo anche dire quale utente ha lanciato i worker se non voglio perdere l'informazione
    #  negli aggiornamenti
    # A T T E N Z I O N E
    in_celery_worker_process = False
    if len(sys.argv) > 0 and sys.argv[0].endswith('celery') and 'worker' in sys.argv:
        in_celery_worker_process = True

    if settings.TESTING:
        return 'User non presente in questa fase di test'
    elif hasattr(_user, 'value'):
        if in_celery_worker_process:
            return 'Worker di Celery per : ' + _user.value
        else:
            return _user.value
    else:
        raise FieldDoesNotExist("La variabile _user non ha atttributo value")


def set_current_username(user):
    _user.value = user


def old_get_current_username():
    # TODO : Attenzione che devo anche dire quale utente ha lanciato i worker se non voglio perdere l'informazione
    #  negli aggiornamenti
    # A T T E N Z I O N E
    in_celery_worker_process = False
    if len(sys.argv) > 0 and sys.argv[0].endswith('celery') and 'worker' in sys.argv:
        in_celery_worker_process = True

    if hasattr(_user, 'value'):
        return _user.value
    elif settings.TESTING:
        return 'User non presente in questa fase di test'
    elif in_celery_worker_process:
        return 'Worker di Celery'
    else:
        raise FieldDoesNotExist("La variabile _user non ha atttributo value")


def si_special_dicts(request):
    """
    Aggiunge al contesto di ogni template :
    1) La lista dei permessi
    2) L'anno formativo che l'utente ha scelto, se l'ha scelto, altrimenti quello di default che va anche a salvare
       nella sessione di lavoro.

    ATTENZIONE che questo è un template context processor (il cui nome viene registato in settings.py) e non un
      middleware context processor per cui quello che aggiunge lo trovo solo nei templates.
    """
    # Se lo trovo nella sessione non devo fare altro, altrimenti lo leggo e lo setto.
    if 'anno_formativo' in request.session:
        anno_formativo = request.session['anno_formativo']
        anno_formativo_pk = request.session['anno_formativo_pk']
    else:
        anno_formativo = '-'
        anno_formativo_pk = -1
    
    # Riporto i dizionari per i template
    return {'siwperms': SiwPermessi.as_dict(), 'anno_formativo': anno_formativo, 'anno_formativo_pk': anno_formativo_pk}


def si_middleware(get_response):
    # One-time configuration and initialization.
    # Attenzione che questo è un middleware context processor E NON un template context processor.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # TODO Come prima cosa controlla se l'utente deve cambiare la password. In questo caso gli permette solo
        # TODO la pagina di cambio password.
        """
        TODO : Da vedere la questione dell'utente che deve cambiare password al prossimo login.
        if request.user.is_authenticated and request.user.profile.must_change_password and not \
              re.match(r'^/settings/password/?', request.path):
            return HttpResponseRedirect('/settings/password/')
        """
        # Imposta l'anno formativo se necessario.
        set_anno_formativo_default(request)
        # Legge e compone la lista dei permessi.
        if not request.user.is_authenticated:
            request.user.si_perms = None
            _user.value = ''
        else:
            request.user.si_perms = get_real_perms(request.user)
            # TODO questo andrebbe loggato !
            """
            print('\n Context processor : user valid')
            print('user' + request.user.username)
            print('user id' + str(request.user.id))
            """
            _user.value = request.user.last_name + ' ' + request.user.first_name
            
        # Spartiacque tra ciò che viene eseguito prima della vista e ciò che viene eseguito dopo.
        response = get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.
        
        return response

    return middleware
