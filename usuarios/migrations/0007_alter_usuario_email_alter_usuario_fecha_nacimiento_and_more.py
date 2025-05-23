# Generated by Django 5.1.7 on 2025-04-19 00:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_alter_usuario_fecha_nacimiento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Este correo electrónico ya está registrado'}, max_length=254, unique=True, verbose_name='Correo electrónico'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='fecha_nacimiento',
            field=models.DateField(help_text='Formato: DD/MM/AAAA', verbose_name='Fecha de Nacimiento'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(help_text='Nombre y apellido separados por espacios', max_length=100, validators=[django.core.validators.RegexValidator(message='El nombre debe contener solo letras y espacios, con al menos nombre y apellido', regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]{2,}(?: [a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]+){1,}$')], verbose_name='Nombre completo'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(help_text='Número de contacto con código de país. Ej: +573001234567', max_length=15, validators=[django.core.validators.RegexValidator(message='Formato de teléfono inválido. Use entre 10 y 15 dígitos', regex='^\\+?[0-9]{10,15}$')], verbose_name='Teléfono'),
        ),
    ]
