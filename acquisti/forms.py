# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django import forms
from .models import AcquistoConOrdine, RipartizioneSpesaPerCDC, AcquistoWeb, RipartizioneAcquistoWebPerCDC
from anagrafe.models import Fornitore
from siw.jqxwidgets import JqxTextInput, JqxComboInput, JqxTextArea, JqxDateInput


class BaseOrdiniForm(forms.ModelForm):
    url_stato_spesa = 'acquisti:ajax_lista_stati_ordine'
    url_tipo_spesa = 'acquisti:ajax_lista_tipo_ordini'
    
    numero_protocollo = forms.CharField(required=False,
                                        widget=JqxTextInput(jqxattrs={'height': 30, 'width': 80, 'minLength': 6}))
    data_ordine = forms.DateField(required=True,
                                  widget=JqxDateInput(jqxattrs={'height': 30, 'width': '150'}))

    stato = forms.ComboField(
        fields=[forms.CharField(), ], required=True, widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 300, 'minLength': 5, 'displayMember': 'descrizione', 'valueMember': "id",
                      'data_adapter_url': url_stato_spesa},
            attrs={'style': 'float: left; margin-right: 5px;'}))

    """
    tipo = forms.ComboField(
        fields=[forms.CharField(), ], required=True, widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 300, 'minLength': 6, 'displayMember': 'descrizione', 'valueMember': "id",
                      'data_adapter_url': url_tipo_spesa},
            attrs={'style': 'float: left; margin-right: 5px;'}))
    """
    imponibile = forms.CharField(required=True,
                                 widget=JqxTextInput(jqxattrs={'height': 30, 'width': 200, 'minLength': 6}))

    aliquota_IVA = forms.CharField(required=True,
                                   widget=JqxTextInput(jqxattrs={'height': 30, 'width': 80, 'minLength': 6}))

    percentuale_IVA_indetraibile = \
        forms.CharField(required=True, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 80, 'minLength': 6}))

    note = forms.CharField(required=False,
                           widget=JqxTextArea(jqxattrs={'height': 200, 'width': 500, 'minLength': 1}))

    class Meta:
        model = AcquistoConOrdine
        fields = ['numero_protocollo', 'data_ordine', 'stato', 'tipo', 'imponibile', 'aliquota_IVA',
                  'percentuale_IVA_indetraibile', 'note']


class AcquistoConOrdineForm(BaseOrdiniForm):
    url_tipo_ordini = 'acquisti:ajax_lista_tipo_ordini'
    url_lista_fornitori = 'acquisti:ajax_lista_fornitori'
    
    tipo = forms.ComboField(
        fields=[forms.CharField(), ], required=True, widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 300, 'minLength': 3, 'displayMember': 'descrizione', 'valueMember': "id",
                      'data_adapter_url': url_tipo_ordini},
            attrs={'style': 'float: left; margin-right: 5px;'}))
    
    fornitore = forms.ModelChoiceField(queryset=Fornitore.objects.all(), required=True, widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 300, 'minLength': 3, 'displayMember': 'azienda__ragione_sociale',
                      'valueMember': 'pk', 'data_adapter_url': url_lista_fornitori},
            attrs={'style': 'float: left; margin-right: 5px;'}))
    
    descrizione = forms.CharField(required=True,
                                  widget=JqxTextInput(jqxattrs={'height': 30, 'width': 500, 'minLength': 6}))
    
    class Meta:
        model = AcquistoConOrdine
        fields = ['numero_protocollo', 'data_ordine', 'stato', 'tipo', 'descrizione', 'fornitore',
                  'imponibile', 'aliquota_IVA', 'percentuale_IVA_indetraibile', 'note']


class AcquistoWebForm(BaseOrdiniForm):
    descrizione = forms.CharField(required=True,
                                  widget=JqxTextInput(jqxattrs={'height': 30, 'width': 500, 'minLength': 6}))
    
    class Meta:
        model = AcquistoWeb
        fields = ['numero_protocollo', 'data_ordine', 'stato', 'descrizione', 'imponibile', 'aliquota_IVA',
                  'percentuale_IVA_indetraibile', 'note']


class RipartizioneForm(forms.ModelForm):
    cdc_txt = forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly': 'True'}))

    percentuale_di_competenza = \
        forms.CharField(required=True, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 80, 'minLength': 6}))
    
    class Meta:
        model = RipartizioneSpesaPerCDC
        fields = ['acquisto', 'cdc', 'percentuale_di_competenza']
        
        widgets = {
            'acquisto': forms.HiddenInput(), 'cdc': forms.HiddenInput(),
        }


class RipartizioneWebForm(forms.ModelForm):
    cdc_txt = forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly': 'True'}))
    
    percentuale_di_competenza = \
        forms.CharField(required=True, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 80, 'minLength': 6}))
    
    class Meta:
        model = RipartizioneSpesaPerCDC
        fields = ['acquisto', 'cdc', 'percentuale_di_competenza']
        
        widgets = {
            'acquisto': forms.HiddenInput(), 'cdc': forms.HiddenInput(),
        }
