from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')  # Accesible en /api/v2/usuarios/

urlpatterns = [
    path('api/v2/', include(router.urls)),
]

#Genera automaticamente las peticiones http