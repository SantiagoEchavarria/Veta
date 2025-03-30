from django.shortcuts import render, redirect
from alertas.models import Alerta
from .models import Medicacion, Paciente
from .forms import MedicacionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def crear_medicacion(request):
    paciente, creado = Paciente.objects.get_or_create(usuario=request.user)
    
    if paciente.nombre != request.user.nombre and request.user.nombre:
        paciente.nombre = request.user.nombre
        paciente.save()
    
    if request.method == "POST":
        form = MedicacionForm(request.POST)
        if form.is_valid():
            medicacion = form.save(commit=False)
            medicacion.paciente = paciente  
            medicacion.save()
            
            # Crear alerta para el paciente
            Alerta.objects.create(
                usuario=paciente.usuario,  # Se usa usuario en lugar de paciente
                mensaje="Nueva medicación agregada",
            )
            
            return redirect("listar_medicacion")  
        else:
            return render(request, 'medicaciones/crear_medicacion.html', {'form': form, 'form_errors': form.errors})
    
    else:
        form = MedicacionForm()
        return render(request, 'medicaciones/crear_medicacion.html', {'form': form})

@login_required
def editar_medicacion(request, id):
    medicacion = get_object_or_404(Medicacion, id=id)

    if request.method == 'POST':
        form = MedicacionForm(request.POST, instance=medicacion)
        if form.is_valid():
            form.save()
            
            # Crear alerta para el paciente al editar la medicación
            Alerta.objects.create(
                usuario=medicacion.paciente.usuario,  # Se usa usuario en lugar de paciente
                mensaje="Se actualizó la medicación",
            )
            
            return redirect('listar_medicacion')
        else:
            return render(request, 'medicaciones/editar_medicacion.html', {'form': form, 'form_errors': form.errors})
    else:
        form = MedicacionForm(instance=medicacion)
        return render(request, 'medicaciones/editar_medicacion.html', {'form': form, "medicacion": medicacion})
    
@login_required 
def listar_medicacion(request):
    paciente = get_object_or_404(Paciente, usuario=request.user)  
    medicacion = Medicacion.objects.filter(paciente=paciente)
    return render(request, "medicaciones/listar_medicacion.html", {"medicaciones": medicacion })

@login_required
def eliminar_medicacion(request, id):
    medicacion = get_object_or_404(Medicacion, pk=id)
    medicacion.delete()
    
    # Crear alerta para el paciente al eliminar la medicación
    Alerta.objects.create(
        usuario=medicacion.paciente.usuario,  # Se usa usuario en lugar de paciente
        mensaje="Se eliminó una medicación",
    )
    
    return redirect('listar_medicacion')
