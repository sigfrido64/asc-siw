# encoding=utf-8
from django.urls import path
from .views import vista1

app_name = 'anagrafe'

"""
    N.B.
    FONDAMENTALE mettere lo slash finale altrimenti ci possono essere errori di risoluzione quando si digita 
    l'url senza slash.
"""
urlpatterns = [
    path('', vista1, name="home"),
    path('1/', vista1, name="v1"),
]
