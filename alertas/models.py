from django.conf import settings
from django.db import models

class Alerta(models.Model):
    TIPO_CHOICES = [
        ('info', 'Información'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,  
        null=True, 
        blank=True
    )
    mensaje = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='info')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.mensaje}"