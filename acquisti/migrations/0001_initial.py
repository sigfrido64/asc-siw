# Generated by Django 2.1.3 on 2019-01-01 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('anagrafe', '0008_fornitore'),
        ('amm', '0015_auto_20181104_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcquistoConOrdine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_uso', models.BooleanField(db_index=True, default=True, verbose_name="Il record è tutt'ora in uso ?")),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('last_user', models.CharField(blank=True, default='', max_length=80)),
                ('numero_protocollo', models.CharField(max_length=10)),
                ('data_ordine', models.DateField()),
                ('stato', models.IntegerField(choices=[(0, 'Bozza'), (10, 'Da Autorizzare'), (20, 'Autorizzato'), (30, 'Inviato'), (40, 'Evaso'), (50, 'Conforme'), (60, 'Liquidato'), (1000, 'Chiuso'), (900, 'ANNULLATO')], default=0)),
                ('tipo', models.IntegerField(choices=[(10, 'Acquisto con Ordine a Fornitore')])),
                ('descrizione', models.TextField()),
                ('imponibile', models.DecimalField(decimal_places=2, max_digits=7)),
                ('aliquota_IVA', models.DecimalField(decimal_places=2, max_digits=4)),
                ('percentuale_IVA_indetraibile', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('protocollo_fattura_fornitore', models.CharField(blank=True, max_length=10)),
                ('conforme', models.BooleanField(default=False)),
                ('note', models.TextField(blank=True)),
                ('dirty', models.BooleanField(default=True)),
                ('iva_comunque_indetraibile', models.DecimalField(decimal_places=2, max_digits=7)),
                ('iva_potenzialmente_detraibile', models.DecimalField(decimal_places=2, max_digits=7)),
                ('cdc_verbose', models.CharField(max_length=50, null=True)),
                ('costo', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('anno_formativo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='amm.AnnoFormativo')),
                ('fornitore', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='anagrafe.Fornitore')),
            ],
            options={
                'verbose_name': 'Acquisto',
                'verbose_name_plural': 'Acquisti',
            },
        ),
        migrations.CreateModel(
            name='RipartizioneSpesaPerCDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_uso', models.BooleanField(db_index=True, default=True, verbose_name="Il record è tutt'ora in uso ?")),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('last_user', models.CharField(blank=True, default='', max_length=80)),
                ('percentuale_di_competenza', models.DecimalField(decimal_places=2, max_digits=5)),
                ('costo_totale', models.DecimalField(decimal_places=2, max_digits=7)),
                ('acquisto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='acquisti.AcquistoConOrdine')),
                ('cdc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='amm.CentroDiCosto')),
            ],
            options={
                'verbose_name': 'Ripartizione Costo su CDC',
                'verbose_name_plural': 'Ripartizione Costo su CDC',
            },
        ),
    ]
