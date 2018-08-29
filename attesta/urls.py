# encoding=utf-8
from django.urls import path
from . import views
from . import ajax

app_name = 'attesta'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('mdl/', views.mdl, name="mdl"),

    # Sezione Ajax
    path('ajax/load-corsi/', ajax.ajax_load_corsi, name='ajax_load_corsi'),
    path('ajax/load-allievi/', ajax.ajax_load_allievi, name='ajax_load_allievi'),
    path('ajax/load-reports/', ajax.ajax_load_reports, name='ajax_load_reports'),

    # Sezione Stampe
    path('stampe/mdl/<str:reportname>/<str:corso>/<int:matricola>/<str:data_stampa>/', views.stampa_mdl,
         name='stampa_mdl'),
]
