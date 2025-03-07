from django.conf import settings
from django.db import models
from usuarios.models import Usuario 
class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150, editable=False)
    tipo_diabetes = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.nombre = self.usuario.nombre
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre