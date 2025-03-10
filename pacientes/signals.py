from django.db.models.signals import post_save
from django.dispatch import receiver
from usuarios.models import Usuario
from .models import Paciente  # Ajusta según la ubicación de tu modelo Paciente

@receiver(post_save, sender=Usuario)
def update_paciente_nombre(sender, instance, **kwargs):
    """
    Actualiza o crea el objeto Paciente asociado al Usuario cada vez que se guarda el Usuario.
    """
    nombre_actualizado = instance.nombre or instance.email
    try:
        paciente = instance.paciente  # Accede al objeto Paciente a través del OneToOneField inverso
        paciente.nombre = nombre_actualizado
        paciente.save()
    except Paciente.DoesNotExist:
        # Si no existe, lo crea
        Paciente.objects.create(usuario=instance, nombre=nombre_actualizado)
