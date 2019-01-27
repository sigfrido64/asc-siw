# coding=utf-8
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from anagrafe.models import TipoTelefonoPersone, TipoMailPersone
from anagrafe.models import PersonaInAzienda, Persona, Fornitore

__author__ = "Pilone Ing. Sigfrido"


@admin.register(TipoTelefonoPersone)
class TipoTelefonoPersoneAdmin(ImportExportModelAdmin):
    exclude = None


@admin.register(TipoMailPersone)
class TipoMailPersoneAdmin(ImportExportModelAdmin):
    exclude = None


@admin.register(PersonaInAzienda)
class PersonaInAziendaAdmin(ImportExportModelAdmin):
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    search_fields = ['persona__cognome']
    exclude = None


@admin.register(Persona)
class PersonaAdmin(ImportExportModelAdmin):
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    search_fields = ['persona__cognome']
    exclude = None


@admin.register(Fornitore)
class FornitoreAdmin(ImportExportModelAdmin):
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    search_fields = ['azienda__ragione_sociale']
    exclude = None
