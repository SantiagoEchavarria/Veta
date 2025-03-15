from django.urls import path,include
from rest_framework import routers
from usuarios import views

routers=routers.DefaultRouter()
routers.register(r'usuarios', views.UsuarioView, 'usuarios')

urlpatterns=[
    path('api/v1/', include(routers.urls) )
]

#Genera automaticamente las peticiones http