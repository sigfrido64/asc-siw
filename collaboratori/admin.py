# coding=utf-8
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Collaboratore, Dipendente

__author__ = "Pilone Ing. Sigfrido"


@admin.register(Collaboratore)
class CollaboratoreAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    list_select_related = True
    autocomplete_fields = ['persona', 'dipendente']
    exclude = None


@admin.register(Dipendente)
class DipendenteAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    list_select_related = True
    search_fields = ['dipendente__cognome']
    exclude = None
