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

    # Agregamos una alerta de prueba para verificar la escritura en la BD
    try:
        mensaje_prueba = f"Alerta de prueba generada al iniciar el servidor - {datetime.now()}"
        print(f"[{datetime.now()}] Intentando crear alerta de prueba...")
        alerta_prueba = Alerta.objects.create(mensaje=mensaje_prueba)
        print(f"[{datetime.now()}] Alerta de prueba creada con ID: {alerta_prueba.id}")
    except Exception as e:
        print(f"[{datetime.now()}] ERROR CRÍTICO: No se pudo crear la alerta de prueba: {e}")
        import traceback
        print(traceback.format_exc())

    while True:
        tiempo_actual = now()  # Este es un datetime con zona horaria (aware)
        hora_actual = tiempo_actual.replace(second=0, microsecond=0)
        print(f"[{datetime.now()}] Verificando medicaciones...")

        medicaciones = Medicacion.objects.all()
        print(f"[{datetime.now()}] Total de medicaciones encontradas: {medicaciones.count()}")
        
        for medicacion in medicaciones:
            if medicacion.hora_inicio is None:
                print(f"[{datetime.now()}] Advertencia: Medicación '{medicacion.nombre_medicamento}' no tiene 'hora_inicio'.")
                continue

            if medicacion.frecuencia is None or medicacion.frecuencia <= 0:
                print(f"[{datetime.now()}] Error: Medicación {medicacion.nombre_medicamento} no tiene frecuencia válida.")
                continue

            print(f"[{datetime.now()}] Procesando medicación: {medicacion.nombre_medicamento}, frecuencia: {medicacion.frecuencia}h, hora inicio: {medicacion.hora_inicio}")

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
                    print(f"[{datetime.now()}] Primera dosis pendiente hoy: {siguiente_alerta}")
                else:
                    # Calcular cuántas dosis completas han pasado desde la hora_inicio
                    horas_transcurridas = (tiempo_actual - hora_inicio_hoy).total_seconds() / 3600
                    dosis_completas = int(horas_transcurridas / medicacion.frecuencia)
                    
                    # Calcular la próxima dosis
                    siguiente_alerta = hora_inicio_hoy + timedelta(hours=medicacion.frecuencia * (dosis_completas + 1))
                    
                    print(f"[{datetime.now()}] Cálculo: {horas_transcurridas:.2f}h transcurridas, {dosis_completas} dosis completas")
                    
                    # Si la siguiente alerta es mañana pero hay otra dosis hoy, ajustar
                    if siguiente_alerta.date() > fecha_base:
                        # Comprobar si hay otra dosis hoy basada en la frecuencia
                        posible_ultima_dosis = hora_inicio_hoy + timedelta(hours=medicacion.frecuencia * dosis_completas)
                        if posible_ultima_dosis.date() == fecha_base and posible_ultima_dosis > tiempo_actual:
                            siguiente_alerta = posible_ultima_dosis
                            print(f"[{datetime.now()}] Ajustado a última dosis de hoy: {siguiente_alerta}")

                print(f"[{datetime.now()}] Siguiente alerta calculada: {siguiente_alerta}")
                print(f"[{datetime.now()}] Hora actual: {tiempo_actual}")
                print(f"[{datetime.now()}] Diferencia: {(tiempo_actual - siguiente_alerta).total_seconds() / 60:.2f} minutos")

                # Comprobar si es hora de la alerta (con un margen de 1 minuto)
                diferencia_minutos = abs((tiempo_actual - siguiente_alerta).total_seconds()) / 60
                
                if diferencia_minutos < 1:  # Margen de 1 minuto para compensar el ciclo de 30 segundos
                    mensaje = f"Es hora de tomar {medicacion.nombre_medicamento} para {medicacion.paciente}"
                    print(f"[{datetime.now()}] CONDICIÓN CUMPLIDA: Creando alerta para {medicacion.nombre_medicamento}")
                    
                    try:
                        nueva_alerta = Alerta.objects.create(mensaje=mensaje)
                        print(f"[{datetime.now()}] Alerta guardada correctamente con ID: {nueva_alerta.id}")
                    except Exception as e:
                        print(f"[{datetime.now()}] ERROR AL GUARDAR ALERTA: {e}")
                        import traceback
                        print(traceback.format_exc())
                else:
                    print(f"[{datetime.now()}] No es momento de alertar (diferencia: {diferencia_minutos:.2f} min)")

                # Forzar una alerta cada 5 minutos para pruebas (solo para medicación Metformina)
                if medicacion.nombre_medicamento == "Metformina" and tiempo_actual.minute % 5 == 0 and tiempo_actual.second < 30:
                    mensaje_prueba = f"ALERTA DE PRUEBA para {medicacion.nombre_medicamento} - {tiempo_actual}"
                    print(f"[{datetime.now()}] Generando alerta de prueba cada 5 minutos")
                    try:
                        alerta_prueba = Alerta.objects.create(mensaje=mensaje_prueba)
                        print(f"[{datetime.now()}] Alerta de prueba creada con ID: {alerta_prueba.id}")
                    except Exception as e:
                        print(f"[{datetime.now()}] ERROR EN ALERTA DE PRUEBA: {e}")
                        import traceback
                        print(traceback.format_exc())

            except Exception as e:
                print(f"[{datetime.now()}] Error en la verificación: {e}")
                import traceback
                print(traceback.format_exc())

        time.sleep(30)  # Espera 30 segundos antes de la próxima verificación


def iniciar_hilo_medicaciones(sender, **kwargs):
    thread = threading.Thread(target=verificar_medicaciones, daemon=True)
    thread.start()
    print("[Django] Hilo de medicaciones iniciado correctamente.")