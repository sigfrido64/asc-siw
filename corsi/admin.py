# coding=utf-8
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import OrdineProduzione, Corso

__author__ = "Pilone Ing. Sigfrido"


@admin.register(OrdineProduzione)
class OrdineProduzioneAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    exclude = None


@admin.register(Corso)
class CorsoAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione', 'data_inizio_annodoy', 'data_fine_annodoy')
    exclude = None
