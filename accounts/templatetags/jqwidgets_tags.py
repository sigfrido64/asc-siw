from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def afield_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def generic_jqxattrs(jqxattrs):
    risultato = ''
    for key, value in jqxattrs.items():
        if isinstance(value, int) or isinstance(value, float):
            risultato += f", {key} : {value}"
        elif isinstance(value, str):
            risultato += f", {key} : '{value}'"

    print('generic jpqx_attrs: ', risultato)
    return mark_safe(risultato)


@register.filter
def combo_jqxattrs(jqxattrs):
    print('combo jqxattrs : ', jqxattrs)
    risultato = ''
    for key, value in jqxattrs.items():
        # Source fa riferimento ad una variabile JavaScript per cui senza apici ''.
        if isinstance(value, int) or isinstance(value, float) or key == 'source':
            risultato += f", {key} : {value}"
        elif isinstance(value, str):
            risultato += f", {key} : '{value}'"

    print('combo jpqx_attrs: ', risultato)
    return mark_safe(risultato)
