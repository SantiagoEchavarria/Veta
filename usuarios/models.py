from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    # Cambia el username por el email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre']

    def __str__(self):
        return self.email

