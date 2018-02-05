# encoding=utf-8

from django.urls import path
from . import views


app_name = 'attesta'
urlpatterns = [
    path('', views.mdl, name="home"),
    
    # Sezione Ajax
    path('ajax/load-corsi/', views.ajax_load_corsi, name='ajax_load_corsi'),
    path('ajax/load-allievi/', views.ajax_load_allievi, name='ajax_load_allievi'),
    
    # Sezione Stampe
    path('stampe/mdl/iscrizione/<str:corso>/<int:matricola>/', views.stampa_mdl_iscrizione,
         name='stampa_iscrizione_mdl'),
]
