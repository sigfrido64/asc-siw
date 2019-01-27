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
    path('ajax/lista_stati_ordine/', ajax.ajax_lista_stati_ordine, name='ajax_lista_stati_ordine'),
    path('ajax/lista_tipo_spesa_2/', ajax.ajax_lista_tipo_spesa_2, name='ajax_lista_tipo_spesa_2'),
    path('ajax/lista_tipo_ordini/', ajax.ajax_lista_tipo_ordini, name='ajax_lista_tipo_ordini'),
    path('ajax/lista_fornitori/', ajax.ajax_lista_fornitori, name='ajax_lista_fornitori'),
    path('ajax/elimina_ripartizione_su_cdc/<str:pk>/', ajax.ajax_elimina_ripartizione_su_cdc,
         name='ajax_elimina_ripartizione_su_cdc'),
    path('ajax/lista_ripartizioni_per_ordine/<str:pk>/', ajax.ajax_lista_ripartizioni_per_ordine,
         name='ajax_lista_ripartizioni_per_ordine'),

    path('ordini/', views.ordini, name='ordini'),
    path('inserimento_cdc/<str:pk>/', views.inserimento_cdc, name='inserimento_cdc'),
    path('inserisce_altra_spesa/', views.inserisce_altra_spesa, name='inserisce_altra_spesa'),
    path('inserisce_ordine/', views.ordine_inserisce, name='ordine_inserisce'),
    path('modifica_ordine/<str:pk>/', views.ordine_modifica, name='ordine_modifica'),
    path('aggiorna/', views.aggiorna_spese, name='aggiorna'),
]