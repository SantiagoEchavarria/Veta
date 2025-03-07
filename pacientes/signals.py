from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from pacientes.models import Paciente

@receiver(post_save, sender=User)
def crear_perfil_paciente(sender, instance, created, **kwargs):
    if created:
        Paciente.objects.create(usuario=instance)
