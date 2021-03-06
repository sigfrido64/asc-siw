# Generated by Django 2.1.5 on 2019-02-10 09:54

from django.db import migrations, models
import django.db.models.deletion
import siw.sig_validators


class Migration(migrations.Migration):

    dependencies = [
        ('amm', '0002_auto_20190128_1300'),
        ('acquisti', '0003_auto_20190202_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcquistoWeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_uso', models.BooleanField(db_index=True, default=True, verbose_name="Il record è tutt'ora in uso ?")),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('last_user', models.CharField(blank=True, default='', max_length=80)),
                ('numero_protocollo', models.CharField(blank=True, default=None, max_length=10, null=True, unique=True)),
                ('data_ordine', models.DateField()),
                ('stato', models.IntegerField(choices=[(0, 'Bozza'), (10, 'Da Autorizzare'), (20, 'Autorizzato'), (30, 'Inviato'), (40, 'Evaso'), (50, 'Conforme'), (60, 'Liquidato'), (1000, 'Chiuso'), (900, 'ANNULLATO')], default=0)),
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
            ],
            options={
                'verbose_name': 'Acquisto su Web',
                'verbose_name_plural': 'Acquisti su Web',
            },
        ),
        migrations.CreateModel(
            name='RipartizioneAcquistoWebPerCDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_uso', models.BooleanField(db_index=True, default=True, verbose_name="Il record è tutt'ora in uso ?")),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('last_user', models.CharField(blank=True, default='', max_length=80)),
                ('percentuale_di_competenza', models.DecimalField(decimal_places=2, max_digits=5, validators=[siw.sig_validators.percentuale_maggiore_zero])),
                ('costo_totale', models.DecimalField(decimal_places=2, max_digits=7)),
                ('acquisto_web', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='acquisti.AcquistoWeb')),
                ('cdc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='amm.CentroDiCosto')),
            ],
            options={
                'verbose_name': 'Ripartizione Acquisto Web su CDC',
                'verbose_name_plural': 'Ripartizione Acquisto Web su CDC',
            },
        ),
        migrations.AlterField(
            model_name='ripartizionespesapercdc',
            name='percentuale_di_competenza',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[siw.sig_validators.percentuale_maggiore_zero]),
        ),
    ]
