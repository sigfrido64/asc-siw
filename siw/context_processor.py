# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from accounts.models import get_real_perms, SiwPermessi
from django.core.exceptions import FieldDoesNotExist
from threading import local
from django.conf import settings
from amm.models.mixins import AnnoFormativo

# Crea un'istanza di _user diversa per ogni thread.
# Così aggiungendo un valore il valore sarà diverso per ogni thread e sarà sempre sincronizzato con lui.
_user = local()


def get_current_username():
    if hasattr(_user, 'value'):
        return _user.value
    elif settings.TESTING:
        return 'User non presente in questa fase di test'
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
    # Se lo trovo nella sessione non devo fare altro.
    if 'anno_formativo' in request.session:
        anno_formativo = request.session['anno_formativo']
        anno_formativo_pk = request.session['anno_formativo_pk']
    else:
        # Altrimenti recupero quello di default.
        anno_formativo_obj = AnnoFormativo.objects.get(default=True)
        anno_formativo = anno_formativo_obj.anno_formativo
        anno_formativo_pk = anno_formativo_obj.pk
        # E lo salvo nella sessione.
        request.session['anno_formativo'] = anno_formativo
        request.session['anno_formativo_pk'] = anno_formativo_pk
    
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
