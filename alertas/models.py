from django.conf import settings
from django.db import models

class Alerta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  null=True, blank=True)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f"Alerta para {self.usuario}: {self.mensaje}"
