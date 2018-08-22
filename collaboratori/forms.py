# coding=utf-8
from django import forms
from django.urls import reverse
from .models import Collaboratore
from siw.jqxwidgets import JqxPasswordInput, JqxTextInput, JqxEmailInput, JqxComboInput, JqxDataAdapter


class NewCollaboratoreForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is in your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    # url = reverse('collaboratori:ajax_lista_tipo_telefoni_persona')
    url = ''
    doc_tel_data_adapter = forms.CharField(
        widget=JqxDataAdapter(
            jqxattrs={'datafields': ('descrizione_telefono', 'pk'),
                      'url': url}))

    tel1 = forms.CharField(widget=JqxTextInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    tel2 = forms.CharField(widget=JqxTextInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    tel3 = forms.CharField(widget=JqxTextInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    tel4 = forms.CharField(widget=JqxTextInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))

    doc_tel1 = forms.ComboField(
        fields=[forms.CharField(), ],
        widget=JqxComboInput(
            jqxattrs={'height': 30, 'width': 350, 'minLength': 1, 'displayMember': 'tipo', 'valueMember': "tipo",
                      'source': doc_tel_data_adapter}))

    class Meta:
        model = Collaboratore
        fields = ['tel1', 'tel2', 'tel3', 'tel4', 'doc_tel1', 'doc_tel2', 'doc_tel3', 'doc_tel4', 'mail1', 'mail2',
                  'doc_mail1', 'doc_mail2', 'note', 'in_uso']
