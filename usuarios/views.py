from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario  
from .forms import UsuarioCreationForm, UsuarioUpdateForm, UsuarioContrasenaForm
from django.contrib import messages

# Vista de inicio
def inicio(request):
    mostrar_modal = request.session.pop('mostrar_modal', False) 
    return render(request, 'usuarios/inicio.html', {'mostrar_modal': mostrar_modal})

# Vista para registrar usuario
def crearSeccion(request):
    if request.method == 'GET': 
        return render(request, 'usuarios/crear_seccion.html', {
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
            return render(request, 'usuarios/crear_seccion.html', {
                'form': form,
                'error': 'Error en el formulario',
                'form_errors': form.errors
            })

# Vista para iniciar sesión
def iniciarSeccion(request):
    if request.method == 'GET': 
        return render(request, 'usuarios/iniciar_seccion.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'usuarios/iniciar_seccion.html', {
                'form': AuthenticationForm(),
                'error': 'Nombre de usuario o contraseña incorrectos'
            })
        else:
            mostrar_modal = False
            
            login(request, user)
            if user.primera_vez: 
                request.session['mostrar_modal'] = True
                user.primera_vez = False  
                user.save() 
        return redirect('inicio')

# Vista para cerrar sesión
@login_required
def cerrarSeccion(request):
    user = request.user
    user.primera_vez = True
    user.save()
    logout(request)
    return redirect('inicio')

@login_required
def editarSeccion(request):
    usuario = request.user  

    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('inicio')  
        else:
            return render(request, 'usuarios/editar_seccion.html', {
                'form': form,
                'error': 'Error al actualizar la información',
                'form_errors': form.errors
            })
    else:
        form = UsuarioUpdateForm(instance=usuario)
        return render(request, 'usuarios/editar_seccion.html', {'form': form})
    
@login_required
def actualizar_contrasena(request):
    if request.method == 'POST':
        form = UsuarioContrasenaForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect('inicio')  
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = UsuarioContrasenaForm(user=request.user)
    
    return render(request, 'usuarios/actualizar_contrasena.html', {'form': form})
