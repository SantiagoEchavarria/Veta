import threading
import time
from datetime import datetime, timedelta
from django.utils.timezone import now, make_aware, is_aware
from .models import Alerta
from medicaciones.models import Medicacion

def verificar_medicaciones():
    """ Revisa si hay medicaciones que necesitan una alerta y, en caso de que
    alertas pasadas no hayan sido creadas (por caída del servidor, por ejemplo),
    las genera sin duplicados. """
    print(f"[{datetime.now()}] Hilo de verificación de medicaciones iniciado...")

    while True:
        tiempo_actual = now()  # Tiempo timezone-aware
        print(f"[{datetime.now()}] Verificando medicaciones...")

        medicaciones = Medicacion.objects.all()
        print(f"[{datetime.now()}] Total de medicaciones encontradas: {medicaciones.count()}")

        for medicacion in medicaciones:
            if not medicacion.hora_inicio or medicacion.frecuencia is None or medicacion.frecuencia <= 0:
                print(f"[{datetime.now()}] Advertencia: Medicación '{medicacion.nombre_medicamento}' tiene datos inválidos.")
                continue

            print(f"[{datetime.now()}] Procesando medicación: {medicacion.nombre_medicamento}, frecuencia: {medicacion.frecuencia}h, hora inicio: {medicacion.hora_inicio}")

            try:
                # Construir el punto base a partir de la fecha actual y la hora de inicio
                base_dosis = datetime.combine(tiempo_actual.date(), medicacion.hora_inicio)
                if not is_aware(base_dosis):
                    base_dosis = make_aware(base_dosis, timezone=tiempo_actual.tzinfo)
                
                # Si el tiempo actual es anterior a la hora de inicio de hoy, asumimos que la serie inició ayer.
                if tiempo_actual < base_dosis:
                    base_dosis -= timedelta(days=1)
                
                # Generar las dosis pasadas: aquellas cuya hora programada es <= tiempo_actual.
                past_doses = []
                dosis = base_dosis
                while dosis <= tiempo_actual:
                    past_doses.append(dosis)
                    dosis += timedelta(hours=medicacion.frecuencia)
                
                # La siguiente dosis es la primera que aún no ha ocurrido.
                siguiente_dosis = dosis
                
                # Procesar las dosis pasadas para generar alertas pendientes.
                for dosis_programada in past_doses:
                    mensaje_dosis = (
                        f"Es hora de tomar {medicacion.nombre_medicamento} para {medicacion.paciente} "
                        f"(programada para {dosis_programada.strftime('%H:%M')})"
                    )
                    # Se verifica si ya existe una alerta para esa dosis.
                    if not Alerta.objects.filter(mensaje=mensaje_dosis).exists():
                        try:
                            nueva_alerta = Alerta.objects.create(mensaje=mensaje_dosis)
                            print(f"[{datetime.now()}] ALERTA GENERADA: {mensaje_dosis} con ID: {nueva_alerta.id}")
                        except Exception as e:
                            print(f"[{datetime.now()}] ERROR AL GUARDAR ALERTA para dosis {dosis_programada.strftime('%H:%M')}: {e}")
                    else:
                        print(f"[{datetime.now()}] Alerta ya existente para dosis programada a las {dosis_programada.strftime('%H:%M')}")
                
                # Procesar la siguiente dosis si estamos en el margen de activación (0 a 1 minuto)
                diferencia_minutos = (siguiente_dosis - tiempo_actual).total_seconds() / 60
                print(f"[{datetime.now()}] Siguiente dosis programada: {siguiente_dosis}")
                print(f"[{datetime.now()}] Diferencia para siguiente alerta: {diferencia_minutos:.2f} minutos")
                if 0 <= diferencia_minutos < 1:
                    mensaje_siguiente = (
                        f"Es hora de tomar {medicacion.nombre_medicamento} para {medicacion.paciente} "
                        f"(programada para {siguiente_dosis.strftime('%H:%M')})"
                    )
                    if not Alerta.objects.filter(mensaje=mensaje_siguiente).exists():
                        print(f"[{datetime.now()}] Creando alerta para la próxima dosis.")
                        try:
                            nueva_alerta = Alerta.objects.create(mensaje=mensaje_siguiente)
                            print(f"[{datetime.now()}] Alerta guardada correctamente con ID: {nueva_alerta.id}")
                        except Exception as e:
                            print(f"[{datetime.now()}] ERROR AL GUARDAR ALERTA para próxima dosis: {e}")
                    else:
                        print(f"[{datetime.now()}] Alerta para la próxima dosis ya existe.")
                        
            except Exception as e:
                print(f"[{datetime.now()}] Error en la verificación: {e}")

        time.sleep(30)  # Espera 30 segundos antes de la próxima verificación

def iniciar_hilo_medicaciones(sender, **kwargs):
    thread = threading.Thread(target=verificar_medicaciones, daemon=True)
    thread.start()
    print("[Django] Hilo de medicaciones iniciado correctamente.")
