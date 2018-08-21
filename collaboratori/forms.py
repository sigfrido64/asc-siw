# coding=utf-8
from django import forms
from .models import Collaboratore


class NewCollaboratoreForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is in your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Collaboratore
        fields = ['tel1', 'tel2', 'tel3', 'tel4', 'doc_tel1', 'doc_tel2', 'doc_tel3', 'doc_tel4', 'mail1', 'mail2',
                  'doc_mail1', 'doc_mail2', 'note', 'in_uso']
