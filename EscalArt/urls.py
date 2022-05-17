from django.urls import path
from .views import ayudacliente, home, perfil_cliente, publicacion, publicacionHome
from .views import perfil
from .views import RegistrarUsuario,ayudacliente


urlpatterns =[
    path('',home, name="home"),
    path('perfil/<id>',perfil, name="perfil"),
    # path('perfil/post/<id>',perfil_post, name="perfil-post"),
    path('registro/',RegistrarUsuario,name="registro"),
    path('ayudacliente',ayudacliente,name="ayudacliente"),
    path('perfil/<artista>/publicacion/<post>',publicacion,name="publicacion"),
    path('home/<artista>/publicacion/<post>',publicacionHome,name="publicacionHome"),
    path('perfilCli/<id>',perfil_cliente,name="perfil_cliente"),

]
