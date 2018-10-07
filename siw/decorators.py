# encoding=utf-8
from functools import wraps
from django.conf import settings
from django.contrib.auth.views import redirect_to_login as dj_redirect_to_login
from django.core.exceptions import PermissionDenied
from accounts.models import has_permission


def has_permission_decorator(permission_name, redirect_to_login=None):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                if has_permission(user, permission_name):
                    return dispatch(request, *args, **kwargs)
                else:
                    raise PermissionDenied
                
            redirect = redirect_to_login
            if redirect is None:
                redirect = getattr(settings, 'LOGIN_URL', False)
            if redirect:
                return dj_redirect_to_login(request.get_full_path())
            else:
                raise PermissionDenied
        return wrapper
    return request_decorator


def ajax_has_permission_decorator(permission_list):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                if has_permission(user, permission_list):
                    return dispatch(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            raise PermissionDenied
        return wrapper
    return request_decorator
