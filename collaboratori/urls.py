# encoding=utf-8
from django.urls import path
from .views import lista_collaboratori_view, mostra_collaboratore_view, propone_inserimento_collaboratore_view
from .views import inserisce_nuovo_collaboratore_view
from .ajax import ajax_load_tutte_persone, ajax_check_persona_for_possible_collaborator, ajax_tipi_telefono_persone
from .ajax import ajax_tipi_mail_persone

app_name = 'collaboratori'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('ajax/load-persone/', ajax_load_tutte_persone, name='ajax_load_tutte_persone'),
    path('ajax/check-persona-for-possibile-collaborator/',
         ajax_check_persona_for_possible_collaborator, name='ajax_check_persona_for_possible_collaborator'),
    path('ajax/lista_tipo_telefoni_persona/',
         ajax_tipi_telefono_persone, name='ajax_lista_tipo_telefoni_persona'),
    path('ajax/lista_tipo_mail_persona/',
         ajax_tipi_mail_persone, name='ajax_lista_tipo_mail_persona'),

    path('anagrafica/lista/', lista_collaboratori_view, name="lista_collaboratori"),
    path('anagrafica/dettaglio/mostra/<int:pk>/', mostra_collaboratore_view, name='mostra_collaboratore'),
    path('anagrafica/propone-inserimento-collaboratore/', propone_inserimento_collaboratore_view,
         name='propone-inserimento-collaboratore'),
    path('anagrafica/inserisce-nuovo/<int:pk_persona>/', inserisce_nuovo_collaboratore_view, name='inserisce_nuovo'),
]
