from django import template
from django.utils.html import mark_safe

# from rolepermissions.checkers import has_permission
from ..models import has_permission


register = template.Library()


@register.filter(name='can')
def can_template_tag(user, permission):
    return has_permission(user, permission)


@register.simple_tag
def descrizione_e_valore(descrizione, valore):
    if descrizione:
        risultato = descrizione + ' : ' + valore
    else:
        risultato = ''
    return mark_safe(risultato)
