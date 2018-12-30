# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.urls import path
from . import views

app_name = 'acquisti'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('', views.spese_home, name='home'),
    path('aggiorna/', views.aggiorna_spese, name='aggiorna'),
]
