# Generated by Django 5.1.7 on 2025-03-30 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicaciones', '0004_alter_medicacion_frecuencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicacion',
            name='hora_inicio',
            field=models.TimeField(blank=True, help_text='Hora en la que se debe tomar la primera dosis', null=True),
        ),
    ]
