import json
from django.utils.timezone import localtime, is_aware, make_aware
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import MedicionGlucosa
from .forms import MedicionGlucosaForm

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
    medicion = get_object_or_404(MedicionGlucosa, id=medicion_id)
    
    if request.method == "POST":
        form = MedicionGlucosaForm(request.POST, instance=medicion)
        if form.is_valid():
            form.save()
            return redirect('lista_mediciones')
    else:
        form = MedicionGlucosaForm(instance=medicion)

    return render(request, 'mediciones/registrar_medicion.html', {'form': form, 'medicion': medicion})

@login_required
def eliminar_medicion(request, medicion_id):
    medicion = get_object_or_404(MedicionGlucosa, id=medicion_id, paciente=request.user)
    
    if request.method == "POST":
        medicion.delete()
    
    return redirect('lista_mediciones')

@login_required
def grafica_mediciones(request):
    mediciones = MedicionGlucosa.objects.filter(paciente=request.user).order_by('fecha_hora')

    # Categorías de medición
    categorias = ["Ayunas", "Postprandial", "Antes de dormir"]
    
    # Diccionario para organizar las mediciones por tipo
    data = {categoria: {"fechas": [], "niveles": []} for categoria in categorias}

    for m in mediciones:
        tipo = m.tipo_medicion  # Asumiendo que tipo_medicion es un string con estos valores
        if tipo in data:  # Evita errores en caso de valores inesperados
            fecha = (localtime(m.fecha_hora) if is_aware(m.fecha_hora) else localtime(make_aware(m.fecha_hora))).strftime("%Y-%m-%d %H:%M")
            data[tipo]["fechas"].append(fecha)
            data[tipo]["niveles"].append(float(m.nivel_glucosa))  # Convertimos Decimal a float

    return render(request, 'mediciones/grafica_mediciones.html', {
        'data_json': json.dumps(data)
    })
