#########
# Serializer

from rest_framework import viewsets
from ..models import Usuario
from .serializer import UsuarioSerializer
from .permissions import EsPropietarioOSuperUsuario  # Importa el permiso personalizado

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [EsPropietarioOSuperUsuario]  # Aplica el permiso

    def get_queryset(self):
        # Superusuarios ven todos los usuarios
        if self.request.user.is_superuser:
            return Usuario.objects.all()
        # Usuarios normales ven solo su propio perfil
        return Usuario.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario actual al crear (si es necesario)
        serializer.save()