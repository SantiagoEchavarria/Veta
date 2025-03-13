from django.contrib import admin
from django.urls import path
from usuarios import views as views_usuarios
from medicaciones import views as views_medicaciones
from django.contrib.auth import views as auth_views
from pacientes import views as views_pacientes

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs de Usuarios:
    path('', views_usuarios.inicio, name='inicio'),
    path('crear_seccion/', views_usuarios.crearSeccion, name='crear_seccion'),
    path('iniciar_seccion/', views_usuarios.iniciarSeccion, name='iniciar_seccion'),
    path('cerrar_seccion/', views_usuarios.cerrarSeccion, name='cerrar_seccion'),
    path('editar_seccion/', views_usuarios.editarSeccion, name='editar_seccion'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # URLs de Medicaciones:
    path('medicaciones/crear/', views_medicaciones.crear_medicacion, name='crear_medicacion'),
    path('medicaciones/listar/', views_medicaciones.listar_medicacion, name='listar_medicacion'),
    
    # URL para pacientes:
    path('mi_paciente/', views_pacientes.mi_detalle_paciente, name='mi_detalle_paciente'),
    path('editar_paciente/', views_pacientes.editar_paciente, name='editar_paciente'),
]
