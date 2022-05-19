from django.urls import path
from .views import  home,PerfilCliente, delete_comision, delete_publicacion, mensajes,perfilArtista,RegistrarUsuario


urlpatterns =[
    path('',home, name="home"),
    path('registro/',RegistrarUsuario,name="registro"),
    path('borrar-publicacion/<id>',delete_publicacion,name='delete_publicacion'),
    path('perfilArtista/<id>',perfilArtista,name='perfilArtista'),
    path('mensajes/', mensajes,name='mensajes'),
    path('mensajes/<id>',mensajes,name='mensajes'),
    path('perfilCliente/<id>',PerfilCliente,name='perfilCliente'),
    path('borrar-comision/<id>',delete_comision,name='delete_comision')

]
