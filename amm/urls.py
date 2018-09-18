# encoding=utf-8
from django.urls import path
from . import views
from .ajax import ajax_centri_di_costo_per_treeview

app_name = 'amm'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('ajax/list-cdc/', ajax_centri_di_costo_per_treeview, name='ajax_centri_di_costo_per_treeview'),
    path('cdc/', views.cdc, name="cdc_home"),
    path('cdc-list/', views.cdc_list, name="cdc_list"),
]
