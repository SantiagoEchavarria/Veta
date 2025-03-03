from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario  # Importa el modelo personalizado
from .forms import UsuarioCreationForm  # Debes crear este formulario

# Vista de inicio
def inicio(request):
    return render(request, 'inicio.html')

# Vista para registrar usuario
def crearSeccion(request):
    if request.method == 'GET': 
        return render(request, 'crear_seccion.html', {
            'form': UsuarioCreationForm()
        })
    else:
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  
            user.save()
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'crear_seccion.html', {
                'form': form,
                'error': 'Error en el formulario',
                'form_errors': form.errors
            })

# Vista para iniciar sesión
def iniciarSeccion(request):
    if request.method == 'GET': 
        return render(request, 'iniciar_seccion.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'iniciar_seccion.html', {
                'form': AuthenticationForm(),
                'error': 'Nombre de usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('inicio')

# Vista para cerrar sesión
@login_required
def cerrarSeccion(request):
    logout(request)
    return redirect('inicio')
