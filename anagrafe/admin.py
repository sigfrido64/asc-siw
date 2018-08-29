# coding=utf-8
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from anagrafe.models import TipoTelefonoPersone, TipoMailPersone

__author__ = "Pilone Ing. Sigfrido"


@admin.register(TipoTelefonoPersone)
class TipoTelefonoPersoneAdmin(ImportExportModelAdmin):
    exclude = None


@admin.register(TipoMailPersone)
class TipoMailPersoneAdmin(ImportExportModelAdmin):
    exclude = None
