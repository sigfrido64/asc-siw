# encoding=utf-8
from django.urls import path
from . import views

app_name = 'corsi'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('lista/', views.corsi_list_home, name='home'),
]
