from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, Fieldset
from .models import Collaboratore

class CollaboratoreForm(forms.ModelForm):
    class Meta:
        model = Collaboratore
        # specify what fields should be used in this form.
        fields = ('tel1', 'tel2', 'tel3', 'tel4')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set layout for fields.
        self.helper = FormHelper()
        # self.helper.form_class = 'form-control-sm'
        self.helper.form_style = 'inline'
        self.helper.layout = Layout(
            Div('tel1', 'tel2', css_class='row'),
            Div('tel3', 'tel4', css_class='row')
        )
        print("Inizializzato")
