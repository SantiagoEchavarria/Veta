from django.db import models

from pacientes.models import Paciente  

class MedicionGlucosa(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)  # Relación con Paciente
    nivel_glucosa = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo_medicion = models.CharField(
        max_length=20,
        choices=[('Ayunas', 'Ayunas'), ('Postprandial', 'Postprandial'), ('Antes de dormir', 'Antes de dormir')]
    )
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.paciente.usuario.username} - {self.nivel_glucosa} mg/dL"