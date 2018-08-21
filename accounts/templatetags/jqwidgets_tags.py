from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def afield_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def jqxattrs(jqxattrs):
    print('jqxattrs : ', jqxattrs)
    risultato = ''
    for key, value in jqxattrs.items():
        if isinstance(value, int) or isinstance(value, float):
            risultato += f", '{key}' : {value}"
        elif isinstance(value, str):
            risultato += f", '{key}' : '{value}'"

    print(risultato)
    return mark_safe(risultato)
