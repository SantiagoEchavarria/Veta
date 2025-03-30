from django.db import models
from pacientes.models import Paciente  

class Medicacion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, editable=False)  # Se asigna automáticamente
    nombre_medicamento = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)
    frecuencia = models.IntegerField()
    hora_inicio = models.TimeField(null=True, blank=True, help_text="Hora en la que se debe tomar la primera dosis")

    def __str__(self):
        return f"{self.nombre_medicamento} - {self.paciente.usuario.username}"
