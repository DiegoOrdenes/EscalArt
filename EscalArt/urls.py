from django.urls import path
from .views import  AddFollower, AddLike, RemoveFollower, UserSearch, home , ayudacliente,  perfil_cliente, publicacion, publicacionHome, tagged
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
    path('perfil/<id>/followers/add', AddFollower.as_view(),name='add-follower'),
    path('perfil/<id>/followers/remove', RemoveFollower.as_view(),name='remove-follower'),
    path('buscar/',UserSearch.as_view(),name='buscar-perfil'),
    path('tag/<slug:slug>/', tagged, name="tagged"),

    # path('borrar-guardado/<id>',delete_guardado,name='delete_guardado'),

]
