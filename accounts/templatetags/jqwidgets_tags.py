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


@register.simple_tag
def siw_field(field):
    class_attuale = field.field.widget.attrs.get('class', '')
    if field.errors:
        class_da_appendere = 'siw-form-control is-invalid'
    else:
        class_da_appendere = 'siw-form-control'
    if class_attuale == '':
        class_nuova = class_da_appendere
    else:
        class_nuova = class_da_appendere + ' ' + class_da_appendere
    field.field.widget.attrs['class'] = class_nuova
    return mark_safe(field.__str__() + field.errors.__str__())
