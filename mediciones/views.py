import json
from django.utils.timezone import localtime, is_aware, make_aware
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import MedicionGlucosa
from .forms import MedicionGlucosaForm
from pacientes.models import Paciente


@login_required
def lista_mediciones(request):
    mediciones = MedicionGlucosa.objects.filter(paciente=request.user).order_by('-fecha_hora')
    return render(request, 'mediciones/lista_mediciones.html', {'mediciones': mediciones})

@login_required
def registrar_medicion(request):
    if request.method == 'POST':
        form = MedicionGlucosaForm(request.POST)
        if form.is_valid():
            medicion = form.save(commit=False)
            medicion.paciente = request.user
            medicion.save()
            return redirect('lista_mediciones')
    else:
        form = MedicionGlucosaForm()
    
    return render(request, 'mediciones/registrar_medicion.html', {'form': form, 'medicion': None})

@login_required
def editar_medicion(request, medicion_id):
    medicion = get_object_or_404(MedicionGlucosa, id=medicion_id, paciente=request.user)
    
    if request.method == "POST":
        form = MedicionGlucosaForm(request.POST, instance=medicion)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.nivel_glucosa = round(instance.nivel_glucosa, 2)
            instance.save()
            return redirect('lista_mediciones')
    else:
        form = MedicionGlucosaForm(instance=medicion, initial={
            'nivel_glucosa': round(medicion.nivel_glucosa, 2)
        })
    
    return render(request, 'mediciones/registrar_medicion.html', {
        'form': form,
        'medicion': medicion
    })

@login_required
def eliminar_medicion(request, medicion_id):
    medicion = get_object_or_404(MedicionGlucosa, id=medicion_id, paciente=request.user)
    
    if request.method == "POST":
        medicion.delete()
    
    return redirect('lista_mediciones')


@login_required
def grafica_mediciones(request):
    mediciones = MedicionGlucosa.objects.filter(paciente=request.user).order_by('fecha_hora')
    paciente = Paciente.objects.get(usuario=request.user)
    
    # Categorías de medición
    categorias = ["Ayunas", "Postprandial", "Antes de dormir"]
    
    # Diccionario para organizar las mediciones por tipo
    data = {categoria: {"fechas": [], "niveles": []} for categoria in categorias}
    
    # Calcular el total, el promedio y la medición más alta de cada tipo de medición
    total_ayunas = 0
    total_postprandial = 0
    total_antes_dormir = 0
    max_ayunas = 0
    max_postprandial = 0
    max_antes_dormir = 0
    count_ayunas = 0
    count_postprandial = 0
    count_antes_dormir = 0

    for m in mediciones:
        tipo = m.tipo_medicion
        if tipo in data:
            fecha = (localtime(m.fecha_hora) if is_aware(m.fecha_hora) else localtime(make_aware(m.fecha_hora))).strftime("%Y-%m-%d %H:%M")
            data[tipo]["fechas"].append(fecha)
            data[tipo]["niveles"].append(float(m.nivel_glucosa))

            # Contar total y cantidad por tipo
            if tipo == "Ayunas":
                total_ayunas += float(m.nivel_glucosa)
                count_ayunas += 1
                max_ayunas = max(max_ayunas, float(m.nivel_glucosa))  # Encontrar el máximo
            elif tipo == "Postprandial":
                total_postprandial += float(m.nivel_glucosa)
                count_postprandial += 1
                max_postprandial = max(max_postprandial, float(m.nivel_glucosa))  # Encontrar el máximo
            elif tipo == "Antes de dormir":
                total_antes_dormir += float(m.nivel_glucosa)
                count_antes_dormir += 1
                max_antes_dormir = max(max_antes_dormir, float(m.nivel_glucosa))  # Encontrar el máximo

    # Promedio de cada tipo de medición
    promedio_ayunas = total_ayunas / count_ayunas if count_ayunas else 0
    promedio_postprandial = total_postprandial / count_postprandial if count_postprandial else 0
    promedio_antes_dormir = total_antes_dormir / count_antes_dormir if count_antes_dormir else 0

    return render(request, 'mediciones/grafica_mediciones.html', {
        'data_json': json.dumps(data),
        'promedio_ayunas': promedio_ayunas,
        'promedio_postprandial': promedio_postprandial,
        'promedio_antes_dormir': promedio_antes_dormir,
        'total_ayunas': count_ayunas,
        'total_postprandial': count_postprandial,
        'total_antes_dormir': count_antes_dormir,
        'max_ayunas': max_ayunas,
        'max_postprandial': max_postprandial,
        'max_antes_dormir': max_antes_dormir,
        'paciente': paciente,
    })

