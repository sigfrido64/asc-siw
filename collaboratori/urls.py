# encoding=utf-8
from django.urls import path
from .views import lista_collaboratori_view, mostra_collaboratore_view, inserisce_collaboratore_view

app_name = 'collaboratori'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('anagrafica/lista/', lista_collaboratori_view, name="lista_collaboratori"),
    path('anagrafica/dettaglio/mostra/<int:id>/', mostra_collaboratore_view, name='mostra_collaboratore'),
    path('anagrafica/inserisce-nuovo/', inserisce_collaboratore_view, name='inserisce_nuovo'),
]
