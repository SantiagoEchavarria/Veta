from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
import hashlib
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario normal con el email, nombre y contraseña.
        """
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password, **extra_fields):
        """
        Crea y guarda un superusuario con el email, nombre y contraseña.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    nombre_validator = RegexValidator(
        regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,}(?: [a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+){1,}$',
        message=_('El nombre debe contener solo letras y espacios, con al menos nombre y apellido')
    )
    
    telefono_validator = RegexValidator(
        regex=r'^\+?[0-9]{10,15}$',
        message=_('Formato de teléfono inválido. Use entre 10 y 15 dígitos')
    )

    primera_vez = models.BooleanField(default=True)
    username = None
    nombre = models.CharField(
        max_length=100,
        validators=[nombre_validator],
        verbose_name=_('Nombre completo'),
        help_text=_('Nombre y apellido separados por espacios')
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_('Correo electrónico'),
        error_messages={
            'unique': _('Este correo electrónico ya está registrado')
        }
    )
    telefono = models.CharField(
        max_length=15,
        validators=[telefono_validator],
        verbose_name=_("Teléfono"),
        help_text=_("Número de contacto con código de país. Ej: +573001234567")
    )
    fecha_nacimiento = models.DateField(
        verbose_name=_("Fecha de Nacimiento"),
        help_text=_("Formato: DD/MM/AAAA")
    )

    objects = UsuarioManager()  # Asigna el gestor personalizado

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email

    def get_gravatar_url(self, size=100):
        email_hash = hashlib.md5(self.email.strip().lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"