# coding=utf-8
from django.http import HttpResponse
from .tasks import allinea_aziende_task, allinea_persone_task, allinea_contatti_aziende_task
from celery import group, chain
from siw.context_processor import get_current_username


def allinea_tutto_da_sql_server_view(request):
    user = get_current_username()
    # Vado a leggere gli elementi dal data base SQL Server.
    # allinea_aziende_task.delay()
    contatti_e_persone = group(allinea_persone_task.si(user), allinea_contatti_aziende_task.si(user))
    lavoro = chain(allinea_aziende_task.si(user), contatti_e_persone)
    lavoro.apply_async()
    return HttpResponse("Processo lanciato in background")
