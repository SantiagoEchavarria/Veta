from django.db import models
from django.contrib.auth import get_user_model

class MedicionGlucosa(models.Model):
    TIPO_MEDICION_CHOICES = [
        ('Ayunas', 'Ayunas'),
        ('Postprandial', 'Postprandial'),
        ('Antes de dormir', 'Antes de dormir'),
    ]

    paciente = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    nivel_glucosa = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_hora = models.DateTimeField()
    tipo_medicion = models.CharField(max_length=20, choices=TIPO_MEDICION_CHOICES)
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.paciente} - {self.nivel_glucosa} mg/dL - {self.tipo_medicion}"