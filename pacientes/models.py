from django.conf import settings
from django.db import models

class Paciente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    tipo_diabetes = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.username
