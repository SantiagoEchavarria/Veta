from django.core.management.base import BaseCommand
from mediciones.models import MedicionGlucosa
from django.contrib.auth import get_user_model

# Ejecuta el script en la terminal con: python manage.py script_crear_mediciones

class Command(BaseCommand):
    help = 'Crea mediciones de glucosa desde la consola'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Obtener datos de entrada
        usuario_id = 11 #input("ID del usuario/paciente: ")
        glucosa = float(85) #float(input("Nivel de glucosa (ej: 95.50): "))
        tipo = "Postprandial" #input("Tipo (Ayunas/Postprandial/Antes de dormir): ")
        notas = "Nada" #input("Notas adicionales (opcional): ")

        # Crear registro
        try:
            usuario = User.objects.get(id=usuario_id)
            MedicionGlucosa.objects.create(
                paciente=usuario,
                nivel_glucosa=glucosa,
                tipo_medicion=tipo,
                notas=notas
            )
            self.stdout.write(self.style.SUCCESS('Medición creada exitosamente!'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Usuario no encontrado'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))