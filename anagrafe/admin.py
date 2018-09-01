# coding=utf-8
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from anagrafe.models import TipoTelefonoPersone, TipoMailPersone
from anagrafe.models import PersonaInAzienda

__author__ = "Pilone Ing. Sigfrido"


@admin.register(TipoTelefonoPersone)
class TipoTelefonoPersoneAdmin(ImportExportModelAdmin):
    exclude = None


@admin.register(TipoMailPersone)
class TipoMailPersoneAdmin(ImportExportModelAdmin):
    exclude = None


@admin.register(PersonaInAzienda)
class PersonaInAziendaAdmin(ImportExportModelAdmin):
    search_fields = ['persona__cognome']
    exclude = None
