from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from .models import Alerta
from medicaciones.models import Medicacion, Paciente
from usuarios.models import Usuario as User

class AlertaTestCase(TestCase):
    def setUp(self):
        """Crea datos de prueba"""
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com', 
            password='12345'
        )

        self.paciente = Paciente.objects.create(usuario=self.user, nombre="Paciente de prueba")
        
        Alerta.objects.create(usuario=self.user, mensaje="Alerta de prueba 1")
        Alerta.objects.create(usuario=self.user, mensaje="Alerta de prueba 2")
    
    def test_vista_alertas(self):
        """Prueba si la vista de alertas carga correctamente"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse("vista_alertas"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "alertas/alertas.html")
    
    def test_api_alertas(self):
        """Prueba si la API devuelve alertas en formato JSON"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse("api_alertas"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertEqual(len(data["alertas"]), 2)

    def test_alerta_creada_al_agregar_medicacion(self):
        """Prueba que se cree una alerta al agregar una medicación"""
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse("crear_medicacion"), {
            "nombre": "Medicamento de prueba",
            "dosis": "500mg",
            "frecuencia": "Cada 8 horas"
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras crear la medicación
        
        alerta = Alerta.objects.filter(usuario=self.user).latest("fecha_creacion")
        self.assertEqual(alerta.mensaje, "Nueva medicación agregada")
        self.assertAlmostEqual(alerta.fecha_creacion, now(), delta=5)  # Verifica la hora con 5 segundos de margen