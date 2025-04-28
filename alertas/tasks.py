import threading
import time
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from .models import Alerta
from medicaciones.models import Medicacion


def verificar_medicaciones():
    print(f"[{timezone.now()}] Hilo de verificación de medicaciones iniciado...")

    while True:
        tiempo_actual = timezone.now()
        print(f"\n[{tiempo_actual}] Verificando medicaciones (hora actual)")

        medicaciones = Medicacion.objects.all()
        print(f"[{tiempo_actual}] Total de medicaciones encontradas: {medicaciones.count()}")

        for medicacion in medicaciones:
            if not medicacion.hora_inicio or medicacion.frecuencia is None or medicacion.frecuencia <= 0:
                print(f"[{tiempo_actual}] Advertencia: Medicación '{medicacion.nombre_medicamento}' tiene datos inválidos.")
                continue

            hora_inicio_local = timezone.localtime(medicacion.hora_inicio)
            print(f"\n[{tiempo_actual}] Procesando: {medicacion.nombre_medicamento}")
            print(f"[{tiempo_actual}] Frecuencia: cada {medicacion.frecuencia}h")
            print(f"[{tiempo_actual}] Hora inicio: {hora_inicio_local.strftime('%Y-%m-%d %H:%M')}")

            try:
                # Calcular todas las dosis desde el inicio hasta ahora
                dosis_actual = hora_inicio_local
                while dosis_actual <= tiempo_actual:
                    print(f"[{tiempo_actual}] Dosis pasada: {dosis_actual.strftime('%Y-%m-%d %H:%M')}")
                    dosis_actual += timedelta(hours=medicacion.frecuencia)

                siguiente_dosis = dosis_actual
                tiempo_restante = siguiente_dosis - tiempo_actual
                
                print(f"[{tiempo_actual}] Próxima dosis: {siguiente_dosis.strftime('%Y-%m-%d %H:%M')}")
                print(f"[{tiempo_actual}] Tiempo restante: {tiempo_restante}")

                # Verificar si es hora de generar alerta (dentro del próximo minuto)
                if tiempo_restante <= timedelta(minutes=1):
                    mensaje = (
                        f"Es hora de tomar {medicacion.nombre_medicamento} para {medicacion.paciente} "
                        f"(programada para {siguiente_dosis.strftime('%Y-%m-%d %H:%M')})"
                    )
                    # Obtener el usuario asociado al paciente
                    usuario_alerta = medicacion.paciente.usuario

                    # Evitar alertas duplicadas para el mismo usuario y mensaje
                    if not Alerta.objects.filter(mensaje=mensaje, usuario=usuario_alerta).exists():
                        Alerta.objects.create(usuario=usuario_alerta, mensaje=mensaje)
                        print(f"[{tiempo_actual}] ¡ALERTA GENERADA!: {mensaje} (usuario: {usuario_alerta})")
                    else:
                        print(f"[{tiempo_actual}] Alerta ya existente para esta dosis y usuario")

            except Exception as e:
                print(f"[{tiempo_actual}] Error en la verificación: {str(e)}")

        time.sleep(30)


def iniciar_hilo_medicaciones(sender, **kwargs):
    thread = threading.Thread(target=verificar_medicaciones, daemon=True)
    thread.start()
    print("[Django] Hilo de medicaciones iniciado correctamente.")
