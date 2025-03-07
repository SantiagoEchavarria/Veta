from django.db import models
from pacientes.models import Paciente  

class Medicacion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, editable=False)  # Se asigna automáticamente
    nombre_medicamento = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre_medicamento} - {self.paciente.usuario.username}"
