# coding=utf-8
from django.shortcuts import render
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi


@has_permission_decorator(SiwPermessi.AMM_CDC_READ)
def cdc(request):
    return render(request, 'amm/cdc_list.html')
