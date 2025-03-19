
from rest_framework.documentation import include_docs_urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    UsuarioViewSet,
    LoginAPIView,
    LogoutAPIView,
    CSRFAPIView,
    PasswordResetView,
    ProfileView
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    # Endpoints del ViewSet
    path('v2/', include(router.urls)),
    # Documentación
    path('docs/', include_docs_urls(title="Usuarios API")),
    path('mi-endpoint/', views.mi_api, name='mi_api'),
    # urls.py
    path('auth/csrf/', views.csrf, name='csrf'),  # Nueva ruta
    
    # Autenticación
    path('auth/', include([
        path('csrf/', CSRFAPIView.as_view(), name='csrf'),
        path('login/', LoginAPIView.as_view(), name='login'),
        path('logout/', LogoutAPIView.as_view(), name='logout'),
        path('register/', UsuarioViewSet.as_view({'post': 'create'}), name='register'),
        path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    ])),
    
    # Perfil de usuario
    path('usuarios/me/', ProfileView.as_view(), name='user-profile'),
    
]