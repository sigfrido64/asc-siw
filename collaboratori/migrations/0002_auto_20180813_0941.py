# Generated by Django 2.1 on 2018-08-13 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collaboratori', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaboratore',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='anagrafe.Persona', unique=True),
        ),
    ]