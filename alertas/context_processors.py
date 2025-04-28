from .models import Alerta

def alertas_globales(request):
    if request.user.is_authenticated:
        return {
            'alertas_globales': Alerta.objects.filter(
                usuario=request.user
            ).order_by('-created_at')[:5]
        }
    return {'alertas_globales': []}