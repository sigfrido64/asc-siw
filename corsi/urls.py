# encoding=utf-8
from django.urls import path
from . import views
from . import ajax

app_name = 'corsi'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('ajax_lista_stati_corso/', ajax.ajax_lista_stati_corso, name='ajax_lista_stati_corso'),

    path('lista/', views.corsi_list_home, name='home'),
    path('dettaglio/<str:pk>/', views.corso_dettaglio_view, name='dettaglio_corso'),
    path('inserisce-nuovo/', views.corso_inserisce_view, name='inserisce_nuovo'),
    path('modifica/<str:pk>/', views.corso_modifica_view, name='modifica'),
]
