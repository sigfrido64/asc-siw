# coding=utf-8
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import CentroDiCosto
from .models import Occasionale, Parasubordinato, Autonomo

__author__ = "Pilone Ing. Sigfrido"


@admin.register(CentroDiCosto)
class IniziativaAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    exclude = None


@admin.register(Occasionale)
class OccasionaleAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    list_select_related = True
    exclude = None

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


@admin.register(Parasubordinato)
class ParasubordinatoAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    list_select_related = True
    exclude = None


@admin.register(Autonomo)
class AutonomoAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione')
    list_select_related = True
    autocomplete_fields = ['personainazienda']
    exclude = None
