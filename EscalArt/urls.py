from unicodedata import name
from django.urls import path
from .views import ayudacliente, home
from .views import perfil
from .views import RegistrarUsuario,ayudacliente,perfil_cliente,configuracion


urlpatterns =[
    path('',home, name="home"),
    path('perfil',perfil, name="perfil"),
    path('registro/',RegistrarUsuario,name="registro"),
    path('ayudacliente',ayudacliente,name="ayudacliente"),
    path('perfil_cliente',perfil_cliente,name="perfil_cliente"),
    path('configuracion',configuracion,name="configuracion")
]
