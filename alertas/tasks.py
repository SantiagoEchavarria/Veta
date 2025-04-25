import threading
import time
from datetime import datetime, timedelta
from django.utils.timezone import now, make_aware, is_aware
from .models import Alerta
from medicaciones.models import Medicacion

def verificar_medicaciones():
    print(f"[{datetime.now()}] Hilo de verificación de medicaciones iniciado...")

    while True:
        tiempo_actual = now()
        print(f"[{datetime.now()}] Verificando medicaciones...")

        medicaciones = Medicacion.objects.all()
        print(f"[{datetime.now()}] Total de medicaciones encontradas: {medicaciones.count()}")

        for medicacion in medicaciones:
            if not medicacion.hora_inicio or medicacion.frecuencia is None or medicacion.frecuencia <= 0:
                print(f"[{datetime.now()}] Advertencia: Medicación '{medicacion.nombre_medicamento}' tiene datos inválidos.")
                continue

            print(f"[{datetime.now()}] Procesando medicación: {medicacion.nombre_medicamento}, frecuencia: {medicacion.frecuencia}h, hora inicio: {medicacion.hora_inicio}")

            try:
                # Calcular base_dosis como la combinación de la fecha actual y la hora de inicio
                base_dosis = datetime.combine(tiempo_actual.date(), medicacion.hora_inicio)
                if not is_aware(base_dosis):
                    base_dosis = make_aware(base_dosis, timezone=tiempo_actual.tzinfo)
                
                # Ajustar base_dosis si es necesario
                if tiempo_actual < base_dosis:
                    base_dosis -= timedelta(days=1)
                
                # Considerar la fecha de creación de la medicación
                # Asegurar que created_at es aware (ajustar según tu modelo)
                created_at = medicacion.created_at
                if not is_aware(created_at):
                    created_at = make_aware(created_at, timezone=tiempo_actual.tzinfo)
                
                # La dosis válida más reciente entre base_dosis y created_at
                inicio_valido = max(base_dosis, created_at)
                
                past_doses = []
                dosis = inicio_valido
                while dosis <= tiempo_actual:
                    past_doses.append(dosis)
                    dosis += timedelta(hours=medicacion.frecuencia)
                
                siguiente_dosis = dosis  # Primera dosis futura
                
                # Generar alertas para dosis pasadas válidas
                for dosis_programada in past_doses:
                    mensaje_dosis = (
                        f"Es hora de tomar {medicacion.nombre_medicamento} para {medicacion.paciente} "
                        f"(programada para {dosis_programada.strftime('%Y-%m-%d %H:%M')})"  # Incluir fecha
                    )
                    if not Alerta.objects.filter(mensaje=mensaje_dosis).exists():
                        try:
                            nueva_alerta = Alerta.objects.create(mensaje=mensaje_dosis)
                            print(f"[{datetime.now()}] ALERTA GENERADA: {mensaje_dosis} con ID: {nueva_alerta.id}")
                        except Exception as e:
                            print(f"[{datetime.now()}] ERROR AL GUARDAR ALERTA para dosis {dosis_programada}: {e}")
                    else:
                        print(f"[{datetime.now()}] Alerta ya existente para {dosis_programada}")
                
                # Procesar siguiente dosis si está en el margen
                diferencia_minutos = (siguiente_dosis - tiempo_actual).total_seconds() / 60
                if 0 <= diferencia_minutos < 1:
                    mensaje_siguiente = (
                        f"Es hora de tomar {medicacion.nombre_medicamento} para {medicacion.paciente} "
                        f"(programada para {siguiente_dosis.strftime('%Y-%m-%d %H:%M')})"
                    )
                    if not Alerta.objects.filter(mensaje=mensaje_siguiente).exists():
                        try:
                            nueva_alerta = Alerta.objects.create(mensaje=mensaje_siguiente)
                            print(f"[{datetime.now()}] Alerta próxima dosis creada: {mensaje_siguiente}")
                        except Exception as e:
                            print(f"[{datetime.now()}] ERROR Alerta próxima dosis: {e}")
                    else:
                        print(f"[{datetime.now()}] Alerta próxima dosis ya existe.")
                        
            except Exception as e:
                print(f"[{datetime.now()}] Error en la verificación: {e}")

        time.sleep(30)

def iniciar_hilo_medicaciones(sender, **kwargs):
    thread = threading.Thread(target=verificar_medicaciones, daemon=True)
    thread.start()
    print("[Django] Hilo de medicaciones iniciado correctamente.")