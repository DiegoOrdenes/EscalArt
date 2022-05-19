from django.urls import path
from .views import  AddLike, home , ayudacliente,  perfil_cliente, publicacion, publicacionHome
from .views import perfil
from .views import RegistrarUsuario,ayudacliente,delete_publicacion


urlpatterns =[
    path('',home, name="home"),
    path('perfil/<id>',perfil, name="perfil"),
    # path('perfil/post/<id>',perfil_post, name="perfil-post"),
    path('registro/',RegistrarUsuario,name="registro"),
    path('ayudacliente',ayudacliente,name="ayudacliente"),
    path('perfil/<artista>/publicacion/<post>',publicacion,name="publicacion"),
    path('home/<artista>/publicacion/<post>',publicacionHome,name="publicacionHome"),
    path('perfilCli/<id>',perfil_cliente,name="perfil_cliente"),
    path('borrar-publicacion/<id>',delete_publicacion,name='delete_publicacion'),
    path('publicacion/<int:pk>/like',AddLike.as_view(),name='like'),
    # path('borrar-guardado/<id>',delete_guardado,name='delete_guardado'),

]
