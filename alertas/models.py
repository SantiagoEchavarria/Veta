from django.conf import settings
from django.db import models

class Alerta(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,  
        null=True, 
        blank=True
    )
    mensaje = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Solo necesitas este campo
    
    class Meta:
        ordering = ['-created_at']  # Orden por defecto
        
    def __str__(self):
        return f"Alerta para {self.usuario}: {self.mensaje} ({self.created_at.strftime('%H:%M %d/%m/%Y')})"