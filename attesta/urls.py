# encoding=utf-8

from django.urls import path
from . import views
from . import ajax

app_name = 'attesta'
# Ricordati di mettere lo slash finale altrimenti puoi avere errori di risoluzione quando digiti l'url senza slash.
urlpatterns = [
    path('mdl/', views.mdl, name="mdl"),
    
    # Sezione Ajax
    path('ajax/load-corsi/', ajax.ajax_load_corsi, name='ajax_load_corsi'),
    path('ajax/load-allievi/', ajax.ajax_load_allievi, name='ajax_load_allievi'),
    path('ajax/load-reports/', ajax.ajax_load_reports, name='ajax_load_reports'),
    
    # Sezione Stampe
    path('stampe/mdl/iscrizione/<str:corso>/<int:matricola>/', views.stampa_mdl_iscrizione,
         name='stampa_iscrizione_mdl'),
]
