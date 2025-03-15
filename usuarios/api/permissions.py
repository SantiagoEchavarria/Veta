from rest_framework import permissions

class EsPropietarioOSuperUsuario(permissions.BasePermission):
    
    """
    Permiso personalizado:
    - Superusuarios pueden realizar cualquier acción.
    - Usuarios normales solo pueden ver/editar su propio perfil.
    """
    def has_object_permission(self, request, view, obj):
        # Solo el dueño o un superusuario puede acceder al objeto
        return obj == request.user or request.user.is_superuser

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_superuser  # Solo superusuarios pueden crear
        if view.action == 'list':
            return request.user.is_superuser
        return True