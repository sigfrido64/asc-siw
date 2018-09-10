# Generated by Django 2.1 on 2018-09-10 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amm', '0009_incaricoattivitavarie_incaricodocenza_rilevamentodocenza'),
        ('corsi', '0004_remove_corso_ordine_produzione'),
    ]

    operations = [
        migrations.AddField(
            model_name='corso',
            name='cdc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='amm.CentroDiCosto'),
        ),
    ]
