import threading
import time
from datetime import datetime, timedelta
from django.utils.timezone import now, make_aware, is_aware
from django.db.models import F
from .models import Alerta
from medicaciones.models import Medicacion

def verificar_medicaciones():
    """ Revisa si hay medicaciones que necesitan una alerta. """
    print(f"[{datetime.now()}] Hilo de verificación de medicaciones iniciado...")

    while True:
        tiempo_actual = now()  # Este es un datetime con zona horaria (aware)
        hora_actual = tiempo_actual.replace(second=0, microsecond=0)
        print(f"[{datetime.now()}] Verificando medicaciones...")

        medicaciones = Medicacion.objects.all()
        for medicacion in medicaciones:
            if medicacion.hora_inicio is None:
                print(f"[{datetime.now()}] Advertencia: Medicación '{medicacion.nombre_medicamento}' no tiene 'hora_inicio'.")
                continue

            if medicacion.frecuencia is None or medicacion.frecuencia <= 0:
                print(f"[{datetime.now()}] Error: Medicación {medicacion.nombre_medicamento} no tiene frecuencia válida.")
                continue

            print(f"[{datetime.now()}] Procesando medicación: {medicacion.nombre_medicamento} a las {medicacion.hora_inicio}")

            try:
                # Convertir hora_inicio a un datetime de hoy (con zona horaria)
                fecha_base = tiempo_actual.date()
                hora_inicio_hoy = datetime.combine(fecha_base, medicacion.hora_inicio)
                
                # Asegurar que hora_inicio_hoy tenga zona horaria (aware)
                if not is_aware(hora_inicio_hoy):
                    hora_inicio_hoy = make_aware(hora_inicio_hoy)
                
                # Encontrar la próxima dosis después de la hora actual
                if hora_inicio_hoy > tiempo_actual:
                    # La primera dosis del día aún no ha llegado
                    siguiente_alerta = hora_inicio_hoy
                else:
                    # Calcular cuántas dosis completas han pasado desde la hora_inicio
                    horas_transcurridas = (tiempo_actual - hora_inicio_hoy).total_seconds() / 3600
                    dosis_completas = int(horas_transcurridas / medicacion.frecuencia)
                    
                    # Calcular la próxima dosis
                    siguiente_alerta = hora_inicio_hoy + timedelta(hours=medicacion.frecuencia * (dosis_completas + 1))
                    
                    # Si la siguiente alerta es mañana pero hay otra dosis hoy, ajustar
                    if siguiente_alerta.date() > fecha_base:
                        # Comprobar si hay otra dosis hoy basada en la frecuencia
                        posible_ultima_dosis = hora_inicio_hoy + timedelta(hours=medicacion.frecuencia * dosis_completas)
                        if posible_ultima_dosis.date() == fecha_base and posible_ultima_dosis > tiempo_actual:
                            siguiente_alerta = posible_ultima_dosis

                print(f"[{datetime.now()}] Calculado siguiente alerta: {siguiente_alerta}")

                # Comprobar si es hora de la alerta (con un margen de 1 minuto)
                diferencia_minutos = abs((tiempo_actual - siguiente_alerta).total_seconds()) / 60
                
                if diferencia_minutos < 1:  # Margen de 1 minuto para compensar el ciclo de 30 segundos
                    mensaje = f"Es hora de tomar {medicacion.nombre_medicamento}"
                    print(f"[{datetime.now()}] Creando alerta para {medicacion.nombre_medicamento}")
                    Alerta.objects.create(mensaje=mensaje)
                    print(f"[{datetime.now()}] Alerta guardada correctamente.")

            except Exception as e:
                print(f"[{datetime.now()}] Error en la verificación: {e}")
                import traceback
                print(traceback.format_exc())

        time.sleep(30)  # Espera 30 segundos antes de la próxima verificación


def iniciar_hilo_medicaciones(sender, **kwargs):
    thread = threading.Thread(target=verificar_medicaciones, daemon=True)
    thread.start()
    print("[Django] Hilo de medicaciones iniciado correctamente.")