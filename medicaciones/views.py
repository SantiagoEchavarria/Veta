from django.shortcuts import render, redirect
from .models import Medicacion, Paciente
from .forms import MedicacionForm
from django.contrib.auth.decorators import login_required
  
@login_required
def crear_medicacion(request):
    paciente, creado = Paciente.objects.get_or_create(usuario=request.user)  # Obtener o crear el paciente
    print("El nombre del paciente es: "+paciente.nombre)
    print("El nombre del usuario es: "+request.user.nombre)
    if paciente.nombre != request.user.nombre and request.user.nombre:
        paciente.nombre = request.user.nombre
        paciente.save()

    if request.method == "POST":
        form = MedicacionForm(request.POST)
        if form.is_valid():
            medicacion = form.save(commit=False)
            medicacion.paciente = paciente  
            medicacion.save()
            return redirect("inicio")  
        else:
            return render(request, 'medicaciones/crear_medicacion.html', {'form': form, 'form_errors': form.errors})
    
    else:
        form = MedicacionForm()
        return render(request, 'medicaciones/crear_medicacion.html', {'form': form})
