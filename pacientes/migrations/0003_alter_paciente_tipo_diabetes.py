# Generated by Django 5.1.7 on 2025-03-09 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_paciente_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='tipo_diabetes',
            field=models.CharField(choices=[('Tipo1', 'Tipo1'), ('Tipo2', 'Tipo2'), ('Gestacional', 'Gestacional'), ('Otro', 'Otro')], default='Tipo2', max_length=50),
        ),
    ]
