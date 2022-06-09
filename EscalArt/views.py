from asyncio.windows_events import NULL
from email import message
from hashlib import new
from itertools import count
from tkinter.messagebox import NO
from xml.etree.ElementTree import Comment
from django.db.models import Q
from multiprocessing.spawn import is_forking
from tkinter.tix import Form
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
# from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from taggit.models import Tag
from django.template.defaultfilters import slugify

from EscalArt.forms import ChatForm, ComisionArtistaForm, ComisionClienteForm, EditComArtForm, EditUsuarioForm, ReferenciasForm, ReviewForm,ComentarioForm, FormularioUsuario, SolicitudForm, calificacionForm, editFotoPerfilForm, editPerfilForm, editTagsPerfil, perfilForm, publicacionForm, GuardarPostForm
from .models import Chat, ChatRoom, Comentarios, Comision, Comision_Cliente, EstadoComision, Perfil, Publicacion, Referencia, Solicitud, Usuario, Guardado, Review




# Create your views here.
def ayudacliente(request):
    return render(request,'escalArt/ayudacliente.html')

def sobre_nosotros(request):
    return render(request,'escalArt/sobre_nosotros.html')


def perfil_cliente(request,id):
    try:
        user = Usuario.objects.get(username = id)
    except:
        return redirect(to='perfil_cliente', id=request.user.username )
    list = Perfil.objects.all()
    algo = Perfil.objects.get(idUser = request.user)
    guardados = Guardado.objects.all()
    comisionCli = Comision_Cliente.objects.filter(idCliente = request.user)

    data = {
        'userInfo':user,
        "perfil":list,
        'foto':editFotoPerfilForm(instance = user),
        'edit': editPerfilForm(instance = algo),
        'guardados':guardados,
        "comCli":comisionCli,
    }
    if(request.user != user):
        return redirect(to='perfil_cliente', id=request.user.username )
    


    if request.method == "POST":
        if 'fotoPerfil' in request.POST:
            pfp = request.FILES.get('pfp',None)
            if pfp is None:
                print('no se subio un archivo')
            else:
                print('estas editando tu foto de perfil')
                foto = editFotoPerfilForm(request.POST,request.FILES,instance=user)
                if foto.is_valid():
                    obj =foto.save(commit=False)
                    obj.imagen = request.FILES["pfp"]
                    obj.save()
                else:
                    print(foto.errors)
        elif 'EditHeader' in request.POST:
            header = request.FILES.get('header', None)
            if header is None:
                print('no se subio un archivo')
            else:
                perfil = editPerfilForm(request.POST,request.FILES, instance=algo)
                obj2 = algo.biografia
                print('Estas cambiando el header/banner')
                if perfil.is_valid():
                    print(f'primera bio: {obj2}')
                    obj = perfil.save(commit=False)
                    obj.img_header = request.FILES["header"]
                    obj.biografia = obj2
                    obj.save()
                    print(f'segunda bio: {obj.biografia}')

                else:
                    print(perfil.errors)        
        else:
            print('no se hizo ni un post')
    
    return render(request,'escalArt/perfil_cliente.html',data)

def perfil(request,id):
    
    artista = Usuario.objects.get(username = id)
    reviewForm = ReviewForm()
    if artista.tipoCuenta.tipoCuenta == 'cliente':    
        return redirect(to='perfil_cliente', id=request.user.username )
    post = Publicacion.objects.order_by('-idPublicacion').all()
    list = Perfil.objects.all()
    listArtista = Usuario.objects.all()
    usuario = Perfil.objects.get(idUser = artista.idUser)
    print(usuario.idUser.idUser)
    
    followers =  usuario.seguidores.all()

    following = Perfil.objects.filter(seguidores= artista.idUser )
    following_count = len(following)

    if len(followers) ==0:
        is_following = False

    try:
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
    except:
        is_following = False

    
    try:
        reviews = Review.objects.filter(idPerfil = usuario).order_by('-fechaCreacion')
        rating= reviews.values("rating")
        print(f'ayuda: {rating}')
        cant_datos = len(reviews)
        print(cant_datos)
        suma = 0
        for i in rating:
            print(f'i es: {i}')
            i = i.get('rating')
            suma = suma + i
            print(f'suma for = {suma}')
        print(suma)    
         
          
            
        promedio = suma/cant_datos
        calificacion = round(promedio)

    except:
        calificacion = 0


    numero_de_seguidores = len(followers)   

    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)

        
        

        data = {
            "list":artista,
            "posts":post,

            'form':publicacionForm(),
            'perfil':list,
            'edit': editPerfilForm(instance = algo),
            'foto':editFotoPerfilForm(instance = user),
            "listArt":listArtista,
            # "publi":publi
            'numFollowers':numero_de_seguidores,
            'is_following': is_following,
            'following_count':following_count,
            'reviewForm':reviewForm,
            'calificacion':calificacion,
            'perfilform':calificacionForm(instance = usuario),
            'reviews':reviews,
            'solicitudForm': SolicitudForm(),

        }
    else:
        data = {
            "list":artista,

            "posts":post,

            'form':publicacionForm(),
            'perfil':list,
            "listArt":listArtista,
            'numFollowers':numero_de_seguidores,
            'is_following': is_following,
            'reviewForm':reviewForm,
            'calificacion':calificacion,
            'perfilform':calificacionForm(instance = usuario),

            'reviews':reviews,


            # "publi":publi
        }

    if(request.method=='POST' ):       
        if 'publicar' in request.POST:
            post = request.FILES.get('publi', None)
            print(f'post = {post}')
            
            if post is None:
                print('ayuda algo paso con lo de la imagen :C')
            else:
                print('estas publicando')

                formulario = publicacionForm(request.POST,request.FILES)   


                if formulario.is_valid():
                    publi = formulario.save(commit=False)
                    publi.idUser = request.user
                    publi.imagen = request.FILES.get('publi')
                    
                    publi.save()
                    formulario.save_m2m()
                            
                else:
                    
                    print(formulario.errors)
            
        elif 'editar' in request.POST:
            
            perfil = editPerfilForm(request.POST,request.FILES,instance=algo)
            print('estas editando')
            if perfil.is_valid():
                perfil.save()
            else:
                print(perfil.errors)
        elif 'EditHeader' in request.POST:
            header = request.FILES.get('header', None)
            if header is None:
                print('no se subio un archivo')
            else:
                perfil = editPerfilForm(request.POST,request.FILES, instance=algo)
                obj2 = algo.biografia
                print('Estas cambiando el header/banner')
                if perfil.is_valid():
                    print(f'primera bio: {obj2}')
                    obj = perfil.save(commit=False)
                    obj.img_header = request.FILES["header"]
                    obj.biografia = obj2
                    obj.save()
                    print(f'segunda bio: {obj.biografia}')

                else:
                    print(perfil.errors)
        elif 'fotoPerfil' in request.POST:
            pfp = request.FILES.get('pfp',None)
            if pfp is None:
                print('no se subio un archivo')
            else:
                print('estas editando tu foto de perfil')
                foto = editFotoPerfilForm(request.POST,request.FILES,instance=user)
                if foto.is_valid():
                    obj =foto.save(commit=False)
                    obj.imagen = request.FILES["pfp"]
                    obj.save()
                else:
                    print(foto.errors)
        elif 'enviarReview' in request.POST:
            review = ReviewForm(request.POST)
            perfil = calificacionForm(request.POST, instance = usuario)
            

            if review.is_valid():
                obj = review.save(commit=False)
                obj.idPerfil = usuario
                obj.idUser = request.user
                obj.review = request.POST['review']
                obj.rating = request.POST['rating']
                obj.save()

                reviews = Review.objects.filter(idPerfil = usuario)
                rating= reviews.values("rating")
                # print(f'ayuda: {rating}')
                cant_datos = len(reviews)
                # print(cant_datos)
                suma = 0
                for i in rating:
                    # print(f'i es: {i}')
                    i = i.get('rating')
                    suma = suma + i
                    # print(f'suma for = {suma}')
                print(f'post suma = {suma}')   
                promedio = suma/cant_datos
                    
                data['calificacion'] =round(promedio)
                if perfil.is_valid():  
                    profile = perfil.save(commit=False)                    
                    
                    profile.calificacion = request.POST['calificacion']
                    profile.calificacion = round(promedio)
                    profile.save()
                    data['reviews'] = Review.objects.filter(idPerfil = usuario).order_by('-fechaCreacion')
                else:
                    print(perfil.errors)                
            else:
                print(review.errors)
        elif 'solicitud' in request.POST:
            form = SolicitudForm(request.POST)
        
            if form.is_valid():
                obj = form.save(commit = False)
                obj.idSolicitud = f"{request.user}{artista.username}"
                obj.idCliente = request.user
                obj.usernameArtista = artista.username
                obj.save()
                # return render(request,'escalArt/mensajes.html',data)
            else:
                print(form.errors)
        else:
            print('no se hizo ni un post')        
    
    return render(request, 'escalArt/Perfil_Artista.html',data)

def publicacion(request,artista,post):
    comentarios = Comentarios.objects.filter(idPublicacion = post).order_by('-fechaCreacion')
    Artista = Usuario.objects.get(username = artista)
    publi = Publicacion.objects.get(idPublicacion = post)
    commentForm = ComentarioForm()
    Post = Publicacion.objects.all()
    list = Perfil.objects.all()
    listArtista = Usuario.objects.all()
    try:
        guardado = Guardado.objects.get(idPublicacion = post)
        
    except:
        guardado = None
        print('no se ha guardado la publicacion aun')      
    

    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)
        if guardado is None:
            data = {
                "list":Artista,
                "posts":Post,

                'form':publicacionForm(),
                'perfil':list,
                'edit': editPerfilForm(instance = algo),
                'foto':editFotoPerfilForm(instance = user),
                "listArt":listArtista,
                "publi":publi,
                'guardarPost':GuardarPostForm(),
                'commentForm':commentForm,
                'comentarios':comentarios,

            }
        else:
            data = {
                "list":Artista,
                "posts":Post,

                'form':publicacionForm(),
                'perfil':list,
                'edit': editPerfilForm(instance = algo),
                'foto':editFotoPerfilForm(instance = user),
                "listArt":listArtista,
                "publi":publi,
                'guardarPost':GuardarPostForm(),
                'guardado':guardado,
                'commentForm':commentForm,
                'comentarios':comentarios,

            }
    else:
        data = {
            "list":Artista,

            "posts":Post,

            'form':publicacionForm(),
            'perfil':list,
            "listArt":listArtista,

            "publi":publi,
            'comentarios':comentarios,
            'commentForm':commentForm,

        }
    
    if request.method == 'POST':
        
        if 'guardarPost' in request.POST:
            guardarPost = GuardarPostForm(request.POST)
            if guardarPost.is_valid:
                obj = guardarPost.save(commit=False)
                obj.idGuardado = f'{request.user}-{request.POST["idPost"]}'
                obj.idUser = request.user
                obj.idPublicacion = Publicacion.objects.get(idPublicacion = request.POST["idPost"])
                print(obj.idPublicacion)
                obj.save()
                data['guardado'] = Guardado.objects.get(idPublicacion = obj.idPublicacion)
            else:
                print(guardarPost.errors)
        
        elif 'eliminarPostGuardado' in request.POST:
            guardado = Guardado.objects.get(idPublicacion=post)
            guardado.delete()
            data['guardado'] = None
        elif 'comentar' in request.POST:
            comentario = ComentarioForm(request.POST)
            if comentario.is_valid:
                nuevo_comentario = comentario.save(commit=False)
                nuevo_comentario.idUser = request.user
                nuevo_comentario.idPublicacion = publi
                nuevo_comentario.save()
            else:
                print(comentario.errors)
        else:
            ('ningun post ha coincidido')

    else:
        print('no se ha hecho ni un post')
    
    return render(request,'escalArt/publicacion.html',data)


def publicacionHome(request,artista,post):
    Artista = Usuario.objects.get(username = artista)
    publi = Publicacion.objects.get(idPublicacion = post)
    guardados = Guardado.objects.all()
    comentarios = Comentarios.objects.filter(idPublicacion = post).order_by('-fechaCreacion')
    commentForm = ComentarioForm()
        


    try:
        guardado = Guardado.objects.get(idPublicacion = post)
        
    except:
        guardado = None
        print('no se ha guardado la publicacion aun')

    Post = Publicacion.objects.all()
    list = Perfil.objects.all()
    listArtista = Usuario.objects.all()
    
    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)
        if guardado is None:
            data = {
                "list":Artista,
                "posts":Post,

                'form':publicacionForm(),
                'perfil':list,
                'edit': editPerfilForm(instance = algo),
                'foto':editFotoPerfilForm(instance = user),
                "listArt":listArtista,
                "publi":publi,
                'guardarPost':GuardarPostForm(),
                'guardados':guardados,
                'comentarios':comentarios,
                'commentForm':commentForm,


            }
        else:
            data = {
                "list":Artista,
                "posts":Post,

                'form':publicacionForm(),
                'perfil':list,
                'edit': editPerfilForm(instance = algo),
                'foto':editFotoPerfilForm(instance = user),
                "listArt":listArtista,
                "publi":publi,
                'guardarPost':GuardarPostForm(),
                'guardados':guardados,
                'guardado':guardado,    
                'comentarios':comentarios,
                'commentForm':commentForm,
                          
            }
            
    else:
        data = {
            "list":Artista,

            "posts":Post,

            'form':publicacionForm(),
            'perfil':list,
            "listArt":listArtista,

            "publi":publi,
            'comentarios':comentarios,
            'commentForm':commentForm,
           
        }
    
    if request.method == 'POST':
        if 'guardarPost' in request.POST:
            guardarPost = GuardarPostForm(request.POST)
            if guardarPost.is_valid:
                obj = guardarPost.save(commit=False)
                obj.idGuardado = f'{request.user}-{request.POST["idPost"]}'
                obj.idUser = request.user
                obj.idPublicacion = Publicacion.objects.get(idPublicacion = request.POST["idPost"])
                print(obj.idPublicacion)
                obj.save()
                data['guardado'] = Guardado.objects.get(idPublicacion = obj.idPublicacion)
            else:
                print(guardarPost.errors)
        
        elif 'eliminarPostGuardado' in request.POST:
            guardado = Guardado.objects.get(idPublicacion=post)
            guardado.delete()
            data['guardado'] = None

        elif 'comentar' in request.POST:
            comentario = ComentarioForm(request.POST)
            if comentario.is_valid:
                nuevo_comentario = comentario.save(commit=False)
                nuevo_comentario.idUser = request.user
                nuevo_comentario.idPublicacion = publi
                nuevo_comentario.save()
            else:
                print(comentario.errors)
        else:
            ('ningun post ha coincidido')
        
    else:
        print('no se ha hecho ni un post')
    return render(request,'escalArt/publicacionHome.html',data)


class ResponderComentarioView(View):
    def post(self,request,artista,post_pk,pk,*args,**kwargs):
        post = Publicacion.objects.get(idPublicacion = post_pk)

        parent_comment = Comentarios.objects.get(pk = pk)
        form = ComentarioForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.idUser = request.user
            new_comment.idPublicacion = post
            new_comment.parent = parent_comment
            new_comment.save()
       
        next = request.POST.get('next','/')

        return HttpResponseRedirect(next)
        
def tagged(request, slug):

    tag = get_object_or_404(Tag, slug=slug)
    

    list = Perfil.objects.all()
    post = Publicacion.objects.filter(tags=tag)
    listArtista = Usuario.objects.all()
    common_tags = Tag.objects.all()[:10]

    # print(request.user)
    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)

        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        
        'edit': editPerfilForm(instance = algo),
        'foto':editFotoPerfilForm(instance = user),

        "listArt":listArtista,
        'common_tags':common_tags,
        'tag':tag,

    }
    else:
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        "listArt":listArtista,
        'common_tags':common_tags,
        'tag':tag,
        
    
    }
    return render(request, 'escalArt/index.html', data)

from django.db.models import Count
def home (request):
    list = Perfil.objects.all()
    post = Publicacion.objects.all().annotate(likes=Count('cantLikes')).order_by('-likes')
    listArtista = Usuario.objects.all()
    common_tags = Tag.objects.all()[:10]
    # print(request.user)
    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)

        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        
        'edit': editPerfilForm(instance = algo),
        'foto':editFotoPerfilForm(instance = user),

        "listArt":listArtista,
        'common_tags':common_tags,

    }
    else:
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        "listArt":listArtista,
        'common_tags':common_tags,        
    
    }

    if(request.method=='POST' ):

        if 'editar' in request.POST:
            perfil = editPerfilForm(request.POST,request.FILES,instance=algo)
            print('estas editando')
            if perfil.is_valid():
                perfil.save()
            else:
                print(perfil.errors)
        elif 'publicar' in request.POST:
            print('estas publicando')
            formulario = publicacionForm(request.POST,request.FILES)
            

            if formulario.is_valid():
                obj = formulario.save(commit=False)
                obj.idUser = request.user
                
                obj.save()
                        
            else:
                print('algo paso wn matate')
                print(formulario.errors)
        elif 'fotoPerfil' in request.POST:
            print('estas editando tu foto de perfil')
            foto = editFotoPerfilForm(request.POST,request.FILES,instance=user)
            if foto.is_valid():
                foto.save()
            else:
                print(foto.errors)
        else:
            print('no se hizo ni un post')
        
    return render(request,'escalArt/index.html',data)


def RegistrarUsuario (request):
    list = Perfil.objects.all()
    post = Publicacion.objects.all().annotate(likes=Count('cantLikes')).order_by('-likes')
    listArtista = Usuario.objects.all()
    common_tags = Tag.objects.all()[:10]
    # print(request.user)
    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)

        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        
        'edit': editPerfilForm(instance = algo),
        'foto':editFotoPerfilForm(instance = user),

        "listArt":listArtista,
        'common_tags':common_tags,
        "perfil":perfilForm(),
        'form':FormularioUsuario(),

    }
    else:
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        "listArt":listArtista,
        'common_tags':common_tags, 
        "perfil":perfilForm(),
        'form':FormularioUsuario(),       
    
    }
   
    if(request.method=='POST' ):
        formulario = FormularioUsuario(request.POST)
        perfil = perfilForm(request.POST)      

        if formulario.is_valid():
            obj = formulario.save(commit=False)
            print(f'id: {obj.nombre}')
            
            if perfil.is_valid():
                obj.save()

                obj2 = perfil.save(commit=False)
                obj2.idUser = Usuario.objects.get(nombre = obj.nombre)
                print(f'quesesto: {obj2.idUser}')

                obj2.save()
            else:
                print(perfil.errors)
                exit
            
            return render(request,'escalArt/index.html',data)
                      
        else:
            print('algo paso wn matate')
            print(formulario.errors)
            print(perfil.errors)
    return render(request,'registration/registro.html',data)

# Agregar likes
class AddLike(View):
    def post(self, request, pk, *args, **kwargs):
        post = Publicacion.objects.get(idPublicacion = pk)
        comment = Comentarios.objects.get(pk = pk)
        is_liked = False

        for like in post.cantLikes.all():
            if like == request.user:
                is_liked = True
                break
            
        if not is_liked:
            post.cantLikes.add(request.user)

        if is_liked:
            post.cantLikes.remove(request.user)

        comment_liked = False

        for like in comment.cantLikes.all():
            if like == request.user:
                comment_liked = True
                break
            
        if not comment_liked:
            comment.cantLikes.add(request.user)

        if comment_liked:
            comment.cantLikes.remove(request.user)    
        
        next = request.POST.get('next','/')

        return HttpResponseRedirect(next)

class AddLikeComment(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comentarios.objects.get(pk = pk)
        comment_liked = False

        for like in comment.cantLikes.all():
            if like == request.user:
                comment_liked = True
                break
            
        if not comment_liked:
            comment.cantLikes.add(request.user)

        if comment_liked:
            comment.cantLikes.remove(request.user)    
        
        next = request.POST.get('next','/')

        return HttpResponseRedirect(next)

# Fin agregar likes
# Follows
class AddFollower(View):
    def post(self,request,id,*args,**kwargs):
        profile = Perfil.objects.get(idUser = id)
        profile.seguidores.add(request.user)

        return redirect('perfil', id = profile.idUser.username)

class RemoveFollower(View):
    def post(self,request,id,*args,**kwargs):
        profile = Perfil.objects.get(idUser = id)
        profile.seguidores.remove(request.user)

        return redirect('perfil', id = profile.idUser.username)
# Fin follows
# Buscar
class UserSearch(View):
    def get(self,request,*args,**kwargs):
        try:
            query = self.request.GET.get('query')
            
            if Q(idUser__username__icontains = query):
                lista_perfil = Perfil.objects.filter(
                    Q(idUser__username__icontains = query)
                )
            
            if Q(idUser__nombre__icontains = query):
                lista_perfil = Perfil.objects.filter(
                    Q(idUser__nombre__icontains = query)
                )
            if Q(tags__name__icontains = query):
                lista_post = Publicacion.objects.filter(
                    Q(tags__name__icontains = query)
                )
                lista_perfil_tag = Perfil.objects.filter(
                    Q(tags__name__icontains = query)
                )           
        except:
            lista_perfil = None
            lista_post = None
            lista_perfil_tag = None
        
        data = {
            'lista_perfil':lista_perfil,
            'lista_post':lista_post,
            'lista_perfil_tag':lista_perfil_tag,
        }
        return render(request, 'escalArt/search.html',data)
# Fin buscar
# Chats
class chats(LoginRequiredMixin,View):
    def get(self, request):
        artista = Usuario.objects.get(username = request.user.username)
        cliente = Usuario.objects.all()
        # estadoCom = EstadoComision.objects.get(idEstado = 1)
        solicitud = Solicitud.objects.all()
        referencias = Referencia.objects.all()
        data ={
            'list': artista,
            'sol':solicitud,
            'cli':cliente,
            'comArt':ComisionArtistaForm,
            'comCli':ComisionClienteForm,
            'ref':ReferenciasForm(),
            'refAll': referencias

        }
        return render(request, 'escalArt/chats.html',data)

class Room(LoginRequiredMixin,View):
    def get(self,request,room_name):
        room = ChatRoom.objects.filter(nombre = room_name).first()
        referencias = Referencia.objects.all()

        chats = []
        if room:
            chats = Chat.objects.filter(room=room).order_by('fecha')
        else:
            room = ChatRoom(nombre = room_name)
            room.save()

        artista = Usuario.objects.get(username = request.user.username)
        cliente = Usuario.objects.all()
        # estadoCom = EstadoComision.objects.get(idEstado = 1)
        solicitud = Solicitud.objects.all()
        referencias = Referencia.objects.all()
        soliCli = Solicitud.objects.get(idSolicitud = room_name)
        # print(f'solicitud = {soliCli.idCliente}')

        # users = soliCli.values("idUser")
        # for user in users:
        #     user = user.get('idCliente')
        #     if (user ==  request.user.idUser):
        #         print('no')
        #     else:
        #         cli = user
        #         break
        

        data ={
            'list': artista,
            'sol':solicitud,
            'cli':cliente,
            'comArt':ComisionArtistaForm,
            'comCli':ComisionClienteForm,
            'ref':ReferenciasForm(),
            'refAll': referencias,
            'room_name':room_name,
            'chats':chats,
            'sala':room,
            'cliente':soliCli,
            'refAll':referencias,
            # 'users':users
        }
        return render(request,'escalArt/pruebaRoom.html',data)
    def post(self,request,room_name,*args,**kwargs):
        estadoCom = EstadoComision.objects.get(idEstado = 1)

        if 'referencia' in request.POST:
            print('estas subiendo una referencia')
            referencia = ReferenciasForm(request.POST,request.FILES)
            soliCli = Solicitud.objects.get(idSolicitud = room_name)
            
           
            if referencia.is_valid():
                ref = referencia.save(commit=False)
                ref.img_referencia = request.FILES['img_referencia']
                ref.usernameArtista = soliCli.usernameArtista
                ref.idUser = request.user
                
                ref.save()                
                              
            else:
                print('algo paso wn matate')
                print(referencia.errors)
        elif 'comision' in request.POST:
            comArt = ComisionArtistaForm(request.POST)
            comCli = ComisionClienteForm(request.POST)
            if comArt.is_valid():
                obj = comArt.save(commit = False)
                obj.idEstado = estadoCom
                obj.idArtista = request.user
                
                if comCli.is_valid():
                    obj.save()
                    obj2= comCli.save(commit=False)
                    obj2.idComision = obj
                    
                    obj2.idCliente = Usuario.objects.get(nombre = request.POST['cliente'])
                    obj2.save()
                else:
                    print(comCli.errors)
                
                # return render(request,'escalArt/mensajes.html',data)
            else:
                print(comArt.errors)
            

        next = request.POST.get('next','/')

        return HttpResponseRedirect(next)
# Fin chats

# Datos cliente
def datosCliente(request,id):    
    user = Usuario.objects.get(username = id)
    comCli = Comision_Cliente.objects.filter(idCliente = user)
    listaPerfiles = Perfil.objects.all()
    perfil = Perfil.objects.get(idUser = user.idUser)
    referencias = Referencia.objects.all()
    data = {
        'userInfo':user,
        "perfiles":listaPerfiles,
        'perfil':perfil,
        'referencias':referencias,
        'comCli':comCli,
        
    }
    return render(request, 'escalArt/datosCliente.html',data)
# Fin datos cliente

# estados comision
def estadoComisionArt(request,idCliente,idComision):

    user = Usuario.objects.get(username = idCliente)
    comCli = Comision_Cliente.objects.filter(idCliente = user)
    comision = Comision_Cliente.objects.get(idComision = idComision)
    listaPerfiles = Perfil.objects.all()
    perfil = Perfil.objects.get(idUser = user.idUser)
    referencias = Referencia.objects.all()
    data = {
        'userInfo':user,
        "perfiles":listaPerfiles,
        'perfil':perfil,
        'referencias':referencias,
        'comCli':comCli,
        'comision':comision,
        'form':EditComArtForm()

    }

    if (request.method == 'POST' and 'editar' in request.POST):
        
        comision = Comision.objects.get(idComision = request.POST['comision'])
        comArt = EditComArtForm(request.POST,instance = comision)
        if comArt.is_valid():
            comArt.save()            
       
        else:
            print(comArt.errors)
            
    else:
        print('no esta entrando')
    return render(request, 'escalArt/estadoComisionArt.html',data)


def estadoComisionCli(request,id,idComision):
    try:
        user = Usuario.objects.get(username = id)
    except:
        return redirect(to='perfil_cliente', id=request.user.username )
    list = Perfil.objects.all()
    algo = Perfil.objects.get(idUser = request.user)
    guardados = Guardado.objects.all()
    comisionCli = Comision_Cliente.objects.filter(idCliente = request.user)
    comision = Comision_Cliente.objects.get(idComision = idComision)

    data = {
        'userInfo':user,
        "perfil":list,
        'foto':editFotoPerfilForm(instance = user),
        'edit': editPerfilForm(instance = algo),
        'guardados':guardados,
        "comCli":comisionCli,
        'comision':comision,

    }
    if(request.user != user):
        return redirect(to='perfil_cliente', id=request.user.username )
    
    
    return render(request, 'escalArt/estadoComisionCli.html',data)
# fin estados comision

# delete
def delete_comision(request,id):
    comision = Comision.objects.get(idComision = id)
    comCli = Comision_Cliente.objects.get(idComision = comision)
    idCli = comCli.idCliente.username
    comision.delete()
    
    return redirect(to='datosCliente', id=idCli )

def delete_publicacion(request,id):
    post = Publicacion.objects.get(idPublicacion=id)
    post.delete()

    return redirect(to='home')

#  Fin delete

# Configuraciones

class configuracion (LoginRequiredMixin,View):
    def get(self,request):
        usuario = Usuario.objects.get(idUser = request.user.idUser)        
        common_tags = Tag.objects.all().order_by('name')[:10]
        perfilUser = Perfil.objects.get(idUser = request.user)
        tagsPerfil =[]
        Notags =[]
        tagPerfil = perfilUser.tags.all()
        print(tagPerfil)
        tag= tagPerfil.values("name")
        for i in tag:
            i = i.get('name')
            print(i)
            tagsPerfil.append(i)
        print(tagsPerfil)
        for ctags in common_tags:
            print(ctags)
            if (ctags in tagPerfil):
                print('a')
                pass
            else:
                Notags.append(ctags)
                print(Notags)

        
        data = {
            'usuario':usuario,
            'common_tags':common_tags,
            'perfil':perfilUser,
            'Notags':Notags,
        }       

        return render(request,'escalArt/Configuracion.html',data)
    def post(self,request,*args,**kwargs):
        usuario = Usuario.objects.get(idUser = request.user.idUser)
        perfilUser = Perfil.objects.get(idUser = request.user)
        if request.method == "POST":
            if 'editarPerfil' in request.POST:
                cuenta = EditUsuarioForm(request.POST,instance=usuario)               
                if request.POST['username']:
                    username = request.POST['username']
                else:
                    username = usuario.username
                if request.POST['nombre']:
                    nombre = request.POST['nombre']
                else:
                    nombre = usuario.nombre
                if request.POST['email']:
                    email = request.POST['email']
                else:
                    email = usuario.email              
               
               
                if cuenta.is_valid():
                    obj = cuenta.save(commit=False) 
                    obj.nombre = nombre
                    obj.email = email
                    obj.username = username
                    obj.save()                     
                else:
                    print(f'edit usuario errores: {cuenta.errors}')
            
            
            elif 'editarBio' in request.POST:
                perfil = editPerfilForm(request.POST,request.FILES,instance=perfilUser)
                print('estas editando')
                if perfil.is_valid():
                    obj=perfil.save(commit=False)
                    obj.biografia = request.POST['biografia']
                    obj.save()
                else:
                    print(perfil.errors)

            elif 'editPfp' in request.POST:
                pfp = request.FILES.get('pfp',None)
                if pfp is None:
                    print('no se subio un archivo')
                else:
                    foto = editFotoPerfilForm(request.POST,request.FILES,instance=usuario)
                    if foto.is_valid():
                        obj =foto.save(commit=False)
                        obj.imagen = request.FILES["pfp"]
                        obj.save()
                    else:
                        print(foto.errors)
            elif 'editTags' in request.POST:
                tagsForm = editTagsPerfil(request.POST, instance = perfilUser)
                tagsPerfil = []
                tagPerfil = perfilUser.tags.all()
                tag= tagPerfil.values("name")
                for i in tag:
                    i = i.get('name')
                    print(i)
                    tagsPerfil.append(i)
                print(f'tags en perfil: {tagsPerfil}')
                tagsElegidas = request.POST.getlist('tags')
                showTags = request.POST.get('showTags',False)
                print(tagsElegidas)
                print(showTags)
                if tagsForm.is_valid():
                    obj = tagsForm.save(commit=False)
                    if showTags == 'on':
                        obj.showTags = True
                    else:
                        obj.showTags = False

                    for tagElegida in tagsElegidas:
                        if tagElegida in tagsPerfil:
                            print('ya tienes esta tag')
                        else:
                            perfilUser.tags.add(tagElegida)
                    
                    
                    obj.save()
                    tagsForm.save_m2m()
                else:
                    print(f'error en editar tags: {tagsForm.errors}')    
                # if tagsForm
                
            next = request.POST.get('next','/')
        return HttpResponseRedirect(next)
def seleccionarC(request):
    return render(request, 'escalArt/seleccionarC.html')
# Fin Configuraciones
# Cambiar contrasenna
class cambiar_pass(PasswordChangeView,LoginRequiredMixin,View):
    def get(self,request):
        usuario = Usuario.objects.get(idUser = request.user.idUser)        
        data = {
            'usuario':usuario
        }       

        return render(request,'registration/cambiar_contra_form.html',data)
# Fin cambair contrasenna

# presentacion?
def presentacion(request):
    return render(request, 'escalArt/presentacion.html')
# Fin presentacion?

