# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django import forms
from .models.centri_di_costo import CentroDiCosto
from siw.jqxwidgets import JqxTextInput, JqxTextArea, JqxDateInput, JqxCheckBox


class CdcForm(forms.ModelForm):
    nome = forms.CharField(required=True,
                           widget=JqxTextInput(jqxattrs={'height': 30, 'width': 500, 'minLength': 6}))
    descrizione = forms.CharField(required=True,
                                  widget=JqxTextInput(jqxattrs={'height': 30, 'width': 500, 'minLength': 6}))
    cup = forms.CharField(required=False,
                          widget=JqxTextInput(jqxattrs={'height': 30, 'width': 500, 'minLength': 6}))
    cig = forms.CharField(required=False,
                          widget=JqxTextInput(jqxattrs={'height': 30, 'width': 500, 'minLength': 6}))
    iva_detraibile = forms.BooleanField(required=False, widget=JqxCheckBox(jqxattrs={'height': 30, 'width': 150}))
    note = forms.CharField(required=False,
                           widget=JqxTextArea(jqxattrs={'height': 200, 'width': 500, 'minLength': 1}))
    valido_dal = forms.DateField(required=True,
                                 widget=JqxDateInput(jqxattrs={'height': 30, 'width': '150'}))
    valido_al = forms.DateField(required=True,
                                widget=JqxDateInput(jqxattrs={'height': 30, 'width': '150'}))

    class Meta:
        model = CentroDiCosto
        fields = ['nome', 'descrizione', 'cup', 'cig', 'iva_detraibile', 'note', 'valido_dal', 'valido_al']
