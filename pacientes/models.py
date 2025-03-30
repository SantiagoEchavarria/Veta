from django.db import models
from usuarios.models import Usuario


class TipoDiabetes(models.TextChoices):
    TIPO1 = "Tipo1", "Tipo 1"
    TIPO2 = "Tipo2", "Tipo 2"
    GESTACIONAL = "Gestacional", "Gestacional"
    OTRO = "Otro", "Otro"


class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150, editable=False)  # Se establece automáticamente
    tipo_diabetes = models.CharField(
        max_length=50, choices=TipoDiabetes.choices, default=TipoDiabetes.TIPO2
    )

    def save(self, *args, **kwargs):
        """Asigna el nombre del usuario al paciente antes de guardarlo."""
        self.nombre = self.usuario.nombre
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
