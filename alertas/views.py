from django.http import JsonResponse
from django.shortcuts import render
from .models import Alerta

def vista_alertas(request):
    alertas = Alerta.objects.filter(usuario=request.user).order_by('-created_at')
    return render(request, "alertas/alertas.html", {"alertas": alertas})

def api_alertas(request):
    alertas = list(Alerta.objects.values())  # Convierte QuerySet a lista de diccionarios
    return JsonResponse({"alertas": alertas})