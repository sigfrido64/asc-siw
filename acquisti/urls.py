# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.urls import path
from . import views, ajax

app_name = 'acquisti'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('ajax_lista_stati_spesa/', ajax.ajax_lista_stati_spesa, name='ajax_lista_stati_spesa'),
    path('ajax_lista_tipo_spesa/', ajax.ajax_lista_tipo_spesa, name='ajax_lista_tipo_spesa'),

    path('', views.spese_home, name='home'),
    path('inserisce_nuovo/', views.inserisce_spesa, name='inserisce_spesa'),
    path('aggiorna/', views.aggiorna_spese, name='aggiorna'),
]
