# Generated by Django 2.1 on 2018-09-10 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corsi', '0006_corso_stato_corso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corso',
            name='durata',
            field=models.FloatField(default=8),
        ),
    ]
