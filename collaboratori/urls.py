# encoding=utf-8
from django.urls import path
from .views import lista_collaboratori_view, mostra_collaboratore_view, propone_inserimento_collaboratore_view
from .ajax import ajax_load_tutte_persone, ajax_check_persona_for_possible_collaborator

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

    path('anagrafica/lista/', lista_collaboratori_view, name="lista_collaboratori"),
    path('anagrafica/dettaglio/mostra/<int:pk>/', mostra_collaboratore_view, name='mostra_collaboratore'),
    path('anagrafica/propone-inserimento-collaboratore/', propone_inserimento_collaboratore_view,
         name='propone-inserimento-collaboratore'),
]
