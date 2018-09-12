# Generated by Django 2.1 on 2018-09-11 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amm', '0009_incaricoattivitavarie_incaricodocenza_rilevamentodocenza'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incaricodocenza',
            options={'verbose_name': 'Incarico di Docenza', 'verbose_name_plural': 'Incarichi di Docenza'},
        ),
        migrations.RemoveField(
            model_name='incaricodocenza',
            name='cdc',
        ),
        migrations.AlterField(
            model_name='incaricodocenza',
            name='tipologia_collaboratore',
            field=models.IntegerField(choices=[(0, 'Occasionale'), (1, 'CoCoCo/CoCoPro'), (2, 'Autonomo'), (3, 'Dipendente')], default=None),
        ),
    ]
