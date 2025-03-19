import json
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny
from ..models import Usuario
from .serializer import UsuarioSerializer
from .permissions import EsPropietarioOSuperUsuario  # Asegúrate de tener este archivo
from django.http import JsonResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated


# ViewSet para CRUD de usuarios
class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [EsPropietarioOSuperUsuario]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]  # Permitir registro público
        return super().get_permissions()
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Usuario.objects.all()
        return Usuario.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save()

# Vistas API para autenticación
class CSRFAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({'csrfToken': get_token(request)})

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        if not email or not password:
            return Response(
                {"detail": "Email y contraseña requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, email=email, password=password)
        
        if not user:
            return Response(
                {"detail": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        login(request, user)
        return Response({
            "id": user.id,
            "email": user.email,
            "is_superuser": user.is_superuser
        }, status=status.HTTP_200_OK)
        
class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Sesión cerrada"}, status=status.HTTP_200_OK)
    
def mi_api(request):
    return JsonResponse({"message": "Hola desde Django!"})

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
@permission_classes([AllowAny])
def mi_endpoint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({"status": "success", "data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def csrf(request):
    return JsonResponse({"csrfToken": request.META.get("CSRF_COOKIE")})

class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Lógica para enviar correo de recuperación
        email = request.data.get('email')
        # Implementa tu lógica aquí
        return Response({'detail': 'Instrucciones enviadas al correo'})