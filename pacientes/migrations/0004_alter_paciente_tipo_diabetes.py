# Generated by Django 5.1.6 on 2025-03-30 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0003_alter_paciente_tipo_diabetes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='tipo_diabetes',
            field=models.CharField(choices=[('Tipo1', 'Tipo 1'), ('Tipo2', 'Tipo 2'), ('Gestacional', 'Gestacional'), ('Otro', 'Otro')], default='Tipo2', max_length=50),
        ),
    ]
