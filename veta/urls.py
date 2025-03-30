from django.contrib import admin
from django.urls import path, include
from usuarios import views as views_usuarios
from medicaciones import views as views_medicaciones
from django.contrib.auth import views as auth_views
from pacientes import views as views_pacientes
from mediciones import views as views_mediciones
from alertas import views as views_alertas

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
    
    # URLs para mediciones
    path('mediciones/listar', views_mediciones.lista_mediciones, name='lista_mediciones'),
    path('mediciones/registrar', views_mediciones.registrar_medicion, name='registrar_medicion'),
    path('mediciones/editar/<int:medicion_id>/', views_mediciones.editar_medicion, name='editar_medicion'),
    path('mediciones/eliminar/<int:medicion_id>/', views_mediciones.eliminar_medicion, name='eliminar_medicion'),
    path('mediciones/grafica/', views_mediciones.grafica_mediciones, name='grafica_mediciones'),
    
    #URLs para alertas
    path("alertas/", views_alertas.vista_alertas, name="vista_alertas"),
    path("api/alertas/", views_alertas.api_alertas, name="api_alertas"),
    ]
