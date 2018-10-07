# coding=utf-8
from django import forms
from .models import Corso
from siw.jqxwidgets import JqxTextInput, JqxComboInput, JqxTextArea, JqxCheckBox, JqxNumberInput, JqxDateInput


class NewCorsoForm(forms.ModelForm):
    url_stato_corso = 'corsi:ajax_lista_stati_corso'

    codice_edizione = forms.CharField(required=True,
                                      widget=JqxTextInput(jqxattrs={'height': 30, 'width': 80, 'minLength': 6}))
    denominazione = forms.CharField(required=True,
                                    widget=JqxTextInput(jqxattrs={'height': 30, 'width': 400, 'minLength': 5}))
    durata = forms.IntegerField(required=True,
                                widget=JqxTextInput(jqxattrs={'height': 30, 'width': 50}))
    cdc_txt = forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly': 'True'}))
    stato_corso = forms.ComboField(
        fields=[forms.CharField(), ], required=False,
        widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 150, 'minLength': 5,
                      'displayMember': 'descrizione', 'valueMember': "id",
                      'data_adapter_url': url_stato_corso},
            attrs={'style': 'float: left; margin-right: 5px;'}))
    data_inizio = forms.DateField(required=True,
                                  widget=JqxDateInput(jqxattrs={'height': 30, 'width': '150'}))
    data_fine = forms.DateField(required=True,
                                widget=JqxDateInput(jqxattrs={'height': 30, 'width': '150'}))
    note = forms.CharField(required=False,
                           widget=JqxTextArea(jqxattrs={'height': 200, 'width': 500, 'minLength': 1}))

    class Meta:
        model = Corso
        fields = ['codice_edizione', 'denominazione', 'durata', 'cdc', 'stato_corso', 'note',
                  'data_inizio', 'data_fine']
        widgets = {
            'cdc': forms.HiddenInput(),
        }
