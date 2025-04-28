from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Alerta
from pacientes.models import Paciente

def vista_alertas(request):
    alertas = Alerta.objects.filter(usuario=request.user).order_by('-created_at')
    return render(request, "alertas/alertas.html", {
        "alertas": alertas,
        "show_all": True,
        "alertas_globales": alertas[:5]  # Para mantener consistencia con el dropdown
    })

def api_alertas(request):
    alertas = list(Alerta.objects.values())  # Convierte QuerySet a lista de diccionarios
    return JsonResponse({"alertas": alertas})