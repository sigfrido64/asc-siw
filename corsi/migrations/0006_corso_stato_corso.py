# Generated by Django 2.1 on 2018-09-10 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corsi', '0005_corso_cdc'),
    ]

    operations = [
        migrations.AddField(
            model_name='corso',
            name='stato_corso',
            field=models.IntegerField(choices=[(0, 'Bozza'), (1, 'In Svolgimento'), (2, 'Terminato'), (3, 'Chiuso')], default=0),
        ),
    ]