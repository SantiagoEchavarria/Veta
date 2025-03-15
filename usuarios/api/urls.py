
from rest_framework.documentation import include_docs_urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, LoginAPIView, LogoutAPIView, CSRFAPIView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    # Endpoints del ViewSet
    path('v2/', include(router.urls)),
    
    # Autenticación
    path('auth/csrf/', CSRFAPIView.as_view(), name='csrf'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    
    # Documentación
    path('docs/', include_docs_urls(title="Usuarios API"))
]