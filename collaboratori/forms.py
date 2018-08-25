# coding=utf-8
from django import forms
from .models import Collaboratore
from siw.jqxwidgets import JqxTextInput, JqxComboInput, JqxTextArea


class NewCollaboratoreForm(forms.ModelForm):
    url = 'collaboratori:ajax_lista_tipo_telefoni_persona'

    tel1 = forms.CharField(required=False, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 150, 'minLength': 1}))
    tel2 = forms.CharField(required=False, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 150, 'minLength': 1}))
    tel3 = forms.CharField(required=False, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 150, 'minLength': 1}))
    tel4 = forms.CharField(required=False, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 150, 'minLength': 1}))

    doc_tel1 = forms.ComboField(
        fields=[forms.CharField(), ], required=False,
        widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 150, 'minLength': 1,
                      'displayMember': 'descrizione_telefono', 'valueMember': "descrizione_telefono",
                      'data_adapter_url': url},
            attrs={'style': 'float: left; margin-right: 5px;'}))

    doc_tel2 = forms.ComboField(
        fields=[forms.CharField(), ], required=False,
        widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 150, 'minLength': 1,
                      'displayMember': 'descrizione_telefono', 'valueMember': "descrizione_telefono",
                      'data_adapter_url': url},
            attrs={'style': 'float: left; margin-right: 5px;'}))

    doc_tel3 = forms.ComboField(
        fields=[forms.CharField(), ], required=False,
        widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 150, 'minLength': 1,
                      'displayMember': 'descrizione_telefono', 'valueMember': "descrizione_telefono",
                      'data_adapter_url': url},
            attrs={'style': 'float: left; margin-right: 5px;'}))

    doc_tel4 = forms.ComboField(
        fields=[forms.CharField(), ], required=False,
        widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 150, 'minLength': 1,
                      'displayMember': 'descrizione_telefono', 'valueMember': "descrizione_telefono",
                      'data_adapter_url': url},
            attrs={'style': 'float: left; margin-right: 5px;'}))

    mail1 = forms.CharField(required=False, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 150, 'minLength': 1}))
    mail2 = forms.CharField(required=False, widget=JqxTextInput(jqxattrs={'height': 30, 'width': 150, 'minLength': 1}))

    doc_mail1 = forms.ComboField(
        fields=[forms.CharField(), ], required=False,
        widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 150, 'minLength': 1,
                      'displayMember': 'descrizione_telefono', 'valueMember': "descrizione_telefono",
                      'data_adapter_url': url},
            attrs={'style': 'float: left; margin-right: 5px;'}))

    doc_mail2 = forms.ComboField(
        fields=[forms.CharField(), ], required=False,
        widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 150, 'minLength': 1,
                      'displayMember': 'descrizione_telefono', 'valueMember': "descrizione_telefono",
                      'data_adapter_url': url},
            attrs={'style': 'float: left; margin-right: 5px;'}))

    note = forms.CharField(required=False,
                           widget=JqxTextArea(jqxattrs={'height': 200, 'width': 500, 'minLength': 1}))

    class Meta:
        model = Collaboratore
        fields = ['tel1', 'tel2', 'tel3', 'tel4', 'doc_tel1', 'doc_tel2', 'doc_tel3', 'doc_tel4', 'mail1', 'mail2',
                  'doc_mail1', 'doc_mail2', 'note']
