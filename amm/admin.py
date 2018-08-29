# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Iniziativa, Progetto, SottoProgetto

__author__ = "Pilone Ing. Sigfrido"


@admin.register(Iniziativa)
class IniziativaAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    exclude = None


@admin.register(Progetto)
class ProgettoAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    exclude = None


@admin.register(SottoProgetto)
class SottoProgettoAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    exclude = None

