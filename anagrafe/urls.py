# encoding=utf-8
from django.urls import path
from .views import allinea_persone_view, allinea_aziende_view

app_name = 'anagrafe'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('aggiorna/persone/', allinea_persone_view, name="allinea-persone"),
    path('aggiorna/aziende/', allinea_aziende_view, name="allinea-aziende"),
]
