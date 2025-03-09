from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Paciente

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
