# coding=utf-8
from django.forms.widgets import Widget
from django.template.loader import render_to_string

# Definisco le Classi che possono essere importare da questo modulo.
__all__ = (
    'JqxPasswordInput', 'JqxEmailInput', 'JqxTextInput',
)


class JqxInput(Widget):
    """
        Classe di base per tutti gli <input> JQWidgets.
    """
    
    input_type = None  # Subclasses must define this.
    template_name = 'includes/jq/jqxinput.html'
    
    # Salva i jqxattrs e chiama l'init della classe base.
    def __init__(self, attrs=None, jqxattrs=None):
        self.jqxattrs = {} if jqxattrs is None else jqxattrs.copy()

        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context
    
    def render(self, name, value, attrs=None, **kwargs):
        # Make final attrs.
        final_attrs = self.build_attrs(self.attrs, attrs)
        
        # Crea il context come nella classe base.
        context = self.get_context(name, value, final_attrs)
        
        # Aggiunge jqxattrs
        context['widget']['jqxattrs'] = self.jqxattrs

        return render_to_string(self.template_name, context)


class JqxPasswordInput(JqxInput):
    template_name = 'includes/jq/jqxpassword.html'
    input_type = 'password'


class JqxEmailInput(JqxInput):
    template_name = 'includes/jq/jqxemail.html'
    input_type = 'email'


class JqxTextInput(JqxInput):
    input_type = 'text'


class JqxComboInput(JqxInput):
    template_name = 'includes/jq/jqxcombobox.html'
    input_type = 'combo-box'

    def __init__(self, attrs=None, jqxattrs=None):
        print("Prima di fare il controllo trovo : ", jqxattrs)
        self.data_adapter_url = jqxattrs.pop('url')
        print("DOpo la pulizia : ", jqxattrs)
        if 'source' in jqxattrs:
            print("il nome è : ", jqxattrs['source'])

        super().__init__(attrs, jqxattrs)
        print(self.jqxattrs)
        print(self.attrs)

    def render(self, name, value, attrs=None, **kwargs):
        # Make final attrs.
        final_attrs = self.build_attrs(self.attrs, attrs)

        # Crea il context come nella classe base.
        context = self.get_context(name, value, final_attrs)

        # Aggiunge jqxattrs
        context['widget']['jqxattrs'] = self.jqxattrs
        context['widget']['data_adapter_url'] = self.data_adapter_url

        return render_to_string(self.template_name, context)


class JqxDataAdapter(JqxInput):
    template_name = 'includes/jq/jqxdataadapter.html'
    input_type = 'data_adapter'

    def __init__(self, attrs=None, jqxattrs=None):
        jqxattrs['datatype'] = 'json'

        super().__init__(attrs, jqxattrs)
        print(self.jqxattrs)
