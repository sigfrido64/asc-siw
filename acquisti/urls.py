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
    path('ajax_lista_tipo_spesa_2/', ajax.ajax_lista_tipo_spesa_2, name='ajax_lista_tipo_spesa_2'),
    path('ajax_lista_tipo_spesa_1/', ajax.ajax_lista_tipo_spesa_1, name='ajax_lista_tipo_spesa_1'),

    path('', views.spese_home, name='home'),
    path('inserisce_altra_spesa/', views.inserisce_altra_spesa, name='inserisce_altra_spesa'),
    path('inserisce_ordine_a_fornitore/', views.inserisce_ordine_a_fornitore, name='inserisce_ordine_a_fornitore'),
    path('aggiorna/', views.aggiorna_spese, name='aggiorna'),
]
