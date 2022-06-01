from unicodedata import name
from django.urls import path
from .views import ayudacliente, home
from .views import perfil,seleccionarC,chats
from .views import RegistrarUsuario,ayudacliente,perfil_cliente,configuracion,presentacion,perfil_cliente_2,cambiar_pass


urlpatterns =[
    path('',home, name="home"),
    path('perfil',perfil, name="perfil"),
    path('registro/',RegistrarUsuario,name="registro"),
    path('ayudacliente',ayudacliente,name="ayudacliente"),
    path('perfil_cliente',perfil_cliente,name="perfil_cliente"),
    path('perfil_cliente_2',perfil_cliente_2,name="perfil_cliente_2"),
    path('configuracion',configuracion,name="configuracion"),
    path('seleccionarC',seleccionarC,name="seleccionarC"),
    path('chats',chats,name="chats"),
    path('presentacion',presentacion,name="presentacion"),
    path('cambiar_pass',cambiar_pass,name="cambiar_pass"),
]
