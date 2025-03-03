from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def crearSeccion(request):
    if request.method == 'GET': 
        print('Enviando formulario')
        return render(request, 'crear_seccion.html', {
            'form': UserCreationForm()
        })

    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Verificar si las contraseñas coinciden
        if password1 != password2:
            return HttpResponse('Las contraseñas no coinciden')

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return HttpResponse('El usuario ya existe')

        # Crear el usuario si todo está bien
        user = User.objects.create_user(username=username, password=password1)

        # Autenticar al usuario antes de iniciar sesión
        user = authenticate(username=username, password=password1)

        if user:
            login(request, user)  

        return redirect('inicio')