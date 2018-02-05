# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from .models import get_real_perms, SiwPermessi
from django.http import HttpResponseRedirect
import re





def si_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # Come prima cosa controlla se l'utente deve cambiare la password. In questo caso gli permette solo
        # la pagina di cambio password.
        """
        TODO : Da vedere la questione dell'utente che deve cambiare password al prossimo login.
        if request.user.is_authenticated and request.user.profile.must_change_password and not \
              re.match(r'^/settings/password/?', request.path):
            return HttpResponseRedirect('/settings/password/')
        """
        # Legge e compone la lista dei permessi.
        if not request.user.is_authenticated:
            request.user.si_perms = None
        else:
            request.user.si_perms = get_real_perms(request.user)
        request.siwperm = {'cazzo': 'culo'}
        
        # Spartiacque tra ciò che viene eseguito prima della vista e ciò che viene eseguito dopo.
        response = get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.
        
        return response

    return middleware
