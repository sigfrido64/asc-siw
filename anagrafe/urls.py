# encoding=utf-8
from django.urls import path
from .views import allinea_tutto_da_sql_server_view
from .ajax import ajax_dettaglio_persona_view

app_name = 'anagrafe'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('ajax/dettaglio-persona/<int:pk_persona>/', ajax_dettaglio_persona_view, name="ajax_dettaglio_persona"),

    path('aggiorna/tutto/', allinea_tutto_da_sql_server_view, name="allinea-tutto"),
]
