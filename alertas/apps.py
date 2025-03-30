from django.apps import AppConfig
import threading

class AlertasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "alertas"

    def ready(self):
        print("[Django] Ejecutando ready() de AlertasConfig...")

        from .tasks import verificar_medicaciones  # Importación dentro de ready() para evitar problemas de importación circular

        # Evitar iniciar múltiples hilos si ya hay uno corriendo
        if not any(t.name == "medicaciones" for t in threading.enumerate()):
            thread = threading.Thread(target=verificar_medicaciones, daemon=True, name="medicaciones")
            thread.start()
            print("[Django] Hilo de medicaciones iniciado correctamente.")
