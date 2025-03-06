from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

import hashlib

class Usuario(AbstractUser):
    username = None
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email

    def get_gravatar_url(self, size=100):
        email_hash = hashlib.md5(self.email.strip().lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"

