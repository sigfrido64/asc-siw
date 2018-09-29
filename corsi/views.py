# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi


@has_permission_decorator(SiwPermessi.CORSI_LISTA_READ)
def corsi_list_home(request):
    return HttpResponse("Eccola qui !")
    #return render(request, 'amm/cdc_list.html')
