# Generated by Django 5.1.7 on 2025-03-15 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicaciones', '0003_alter_medicacion_paciente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicacion',
            name='frecuencia',
            field=models.IntegerField(),
        ),
    ]
