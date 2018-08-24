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
    return mark_safe(risultato)


@register.filter
def jqxattrs_data_adapter_fields(jqxattrs):
    # Creo l'insieme dei campi dati che mi servono per il data adapter usando tutti quelli che mi viene richiesto
    # di mostrare.
    campi_dati = set()
    campi_dati.update([jqxattrs['displayMember']])
    campi_dati.update([jqxattrs['valueMember']])

    risultato = '['
    primo = True
    for key in campi_dati:
        if primo:
            risultato += f"{{name : '{key}'}}"
            primo = False
        else:
            risultato += f", {{name : '{key}'}}"
    risultato += ']'
    return mark_safe(risultato)
