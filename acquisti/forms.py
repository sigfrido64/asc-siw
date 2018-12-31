# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django import forms
from .models import Spesa
from siw.jqxwidgets import JqxTextInput, JqxComboInput, JqxTextArea, JqxCheckBox, JqxDateInput


class NewSpesaTipo2Form(forms.ModelForm):
    url_stato_spesa = 'acquisti:ajax_lista_stati_spesa'
    url_tipo_spesa = 'acquisti:ajax_lista_tipo_spesa_2'
    
    numero_protocollo = forms.CharField(required=True,
                                        widget=JqxTextInput(jqxattrs={'height': 30, 'width': 80, 'minLength': 6}))
    data_ordine = forms.DateField(required=True,
                                  widget=JqxDateInput(jqxattrs={'height': 30, 'width': '150'}))

    stato = forms.ComboField(
        fields=[forms.CharField(), ], required=True, widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 300, 'minLength': 5, 'displayMember': 'descrizione', 'valueMember': "id",
                      'data_adapter_url': url_stato_spesa},
            attrs={'style': 'float: left; margin-right: 5px;'}))

    tipo = forms.ComboField(
        fields=[forms.CharField(), ], required=True, widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 300, 'minLength': 6, 'displayMember': 'descrizione', 'valueMember': "id",
                      'data_adapter_url': url_tipo_spesa},
            attrs={'style': 'float: left; margin-right: 5px;'}))

    imponibile = forms.CharField(required=True,
                                 widget=JqxTextInput(jqxattrs={'height': 30, 'width': 200, 'minLength': 6}))

    aliquota_IVA = forms.CharField(required=True,
                                   widget=JqxTextInput(jqxattrs={'height': 30, 'width': 80, 'minLength': 6}))

    percentuale_IVA_indetraibile = \
        forms.CharField(required=True, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 80, 'minLength': 6}))

    note = forms.CharField(required=False,
                           widget=JqxTextArea(jqxattrs={'height': 200, 'width': 500, 'minLength': 1}))

    class Meta:
        model = Spesa
        fields = ['numero_protocollo', 'data_ordine', 'stato', 'tipo', 'imponibile', 'aliquota_IVA',
                  'percentuale_IVA_indetraibile', 'note']


class NewSpesaTipo1Form(NewSpesaTipo2Form):
    url_tipo_spesa = 'acquisti:ajax_lista_tipo_spesa_1'
    
    tipo = forms.ComboField(
        fields=[forms.CharField(), ], required=True, widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 300, 'minLength': 3, 'displayMember': 'descrizione', 'valueMember': "id",
                      'data_adapter_url': url_tipo_spesa},
            attrs={'style': 'float: left; margin-right: 5px;'}))
    
    descrizione = forms.CharField(required=True,
                                  widget=JqxTextInput(jqxattrs={'height': 30, 'width': 500, 'minLength': 6}))
    
    class Meta:
        model = Spesa
        fields = ['numero_protocollo', 'data_ordine', 'stato', 'tipo', 'descrizione', 'imponibile', 'aliquota_IVA',
                  'percentuale_IVA_indetraibile', 'note']
