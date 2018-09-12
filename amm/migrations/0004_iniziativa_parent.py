# Generated by Django 2.1 on 2018-09-03 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amm', '0003_autonomo_occasionale_parasubordinato'),
    ]

    operations = [
        migrations.AddField(
            model_name='iniziativa',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='amm.Iniziativa'),
        ),
    ]
