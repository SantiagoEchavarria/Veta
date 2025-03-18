from django.contrib import admin
from django.urls import path,include
from usuarios import views as views_usuarios
from medicaciones import views as views_medicaciones
from django.contrib.auth import views as auth_views
from pacientes import views as views_pacientes
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs de Usuarios:
    path('', views_usuarios.inicio, name='inicio'),
    # Sirve el index.html de React para todas las rutas no API
    path('', TemplateView.as_view(template_name='index.html')),
    path('crear_seccion/', views_usuarios.crearSeccion, name='crear_seccion'),
    path('iniciar_seccion/', views_usuarios.iniciarSeccion, name='iniciar_seccion'),
    path('cerrar_seccion/', views_usuarios.cerrarSeccion, name='cerrar_seccion'),
    path('editar_seccion/', views_usuarios.editarSeccion, name='editar_seccion'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('actualizar-contrasena/', views_usuarios.actualizar_contrasena, name='actualizar_contrasena'),
    
    # Incluye las URLs de la API bajo /api/
    path('api/', include('usuarios.api.urls')),

    # URLs de Medicaciones:
    path('medicaciones/crear/', views_medicaciones.crear_medicacion, name='crear_medicacion'),
    path('medicaciones/listar/', views_medicaciones.listar_medicacion, name='listar_medicacion'),
    path('medicaciones/editar/<int:id>', views_medicaciones.editar_medicacion, name='editar_medicacion'),
    path('medicaciones/eliminar/<int:id>/', views_medicaciones.eliminar_medicacion, name='eliminar_medicacion'),
    
    # URL para pacientes:
    path('mi_paciente/', views_pacientes.mi_detalle_paciente, name='mi_detalle_paciente'),
    path('editar_paciente/', views_pacientes.editar_paciente, name='editar_paciente'),

    
]
