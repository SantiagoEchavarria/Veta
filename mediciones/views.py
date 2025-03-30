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


