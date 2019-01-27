# encoding=utf-8
from django.urls import path
from . import views
from .ajax import ajax_centri_di_costo_per_treeview, ajax_centro_di_costo_dettaglio, ajax_load_af, ajax_set_af, \
    ajax_insert_cdc_figlio

app_name = 'amm'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('ajax/list-cdc/', ajax_centri_di_costo_per_treeview, name='ajax_centri_di_costo_per_treeview'),
    path('ajax/detail-cdc/', ajax_centro_di_costo_dettaglio, name='ajax_centro_di_costo_dettaglio'),
    path('ajax/insert-cdc/<str:pk_parent>/', ajax_insert_cdc_figlio, name='ajax_insert_cdc_figlio'),
    path('ajax_load_af/', ajax_load_af, name='ajax_load_af'),
    path('ajax_set_af/', ajax_set_af, name='ajax_set_af'),
    path('cdc/', views.cdc, name="cdc_home"),
]
