from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Paciente
from .forms import PacienteUpdateForm

@login_required
def mi_detalle_paciente(request):
    try:
        paciente = Paciente.objects.get(usuario=request.user)
    except Paciente.DoesNotExist:
        # Crear automáticamente el perfil de paciente para el usuario
        paciente = Paciente.objects.create(usuario=request.user)
        # Opcionalmente, redirigir a una página para que el usuario complete su información
        # return redirect('completar_perfil')
    
    context = {'paciente': paciente}
    return render(request, 'pacientes/pacientes_detalles.html', context)


@login_required
def editar_paciente(request):
    paciente = Paciente.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = PacienteUpdateForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('mi_detalle_paciente')  # Redirige a la página de inicio después de la edición
        else:
            return render(request, 'pacientes/editar_pacientes.html', {
                'form': form,
                'error': 'Error al actualizar la información',
                'form_errors': form.errors
            })
    else:
        form = PacienteUpdateForm(instance=paciente)
        return render(request, 'pacientes/editar_pacientes.html', {'form': form})
