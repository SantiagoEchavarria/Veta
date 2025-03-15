from rest_framework import permissions

class EsPropietarioOSuperUsuario(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Usuario normal: solo su propio perfil | Superuser: acceso total
        return obj == request.user or request.user.is_superuser

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_superuser  # Solo superusers listan todos
        return True  # Cualquiera puede crear (si la vista lo permite)