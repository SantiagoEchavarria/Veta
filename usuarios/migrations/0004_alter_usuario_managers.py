# Generated by Django 5.1.7 on 2025-03-10 16:24

import usuarios.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_remove_usuario_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usuario',
            managers=[
                ('objects', usuarios.models.UsuarioManager()),
            ],
        ),
    ]
