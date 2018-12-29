# coding=utf-8
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Spesa, RipartizioneSpesaPerCDC


@admin.register(Spesa)
class SpesaAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione', 'costo', 'dirty',
                       'iva_comunque_indetraibile', 'iva_potenzialmente_detraibile')
    list_select_related = True
    exclude = None


@admin.register(RipartizioneSpesaPerCDC)
class RipartizioneSpesePerCDCAdmin(ImportExportModelAdmin):
    # Mostro in readonly l'utente che ha fatto l'ultima modifica
    # Metto in readonly anche le due date perchè per loro natura ereditano Editable = False. Così invece le vedo in
    # read only che mi garantisce anche che non possano essere modificate.
    readonly_fields = ('last_user', 'data_aggiornamento', 'data_creazione', 'costo_totale')
    list_select_related = True
    exclude = None
