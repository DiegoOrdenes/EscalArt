from asyncio.windows_events import NULL
from email import message
from tkinter.tix import Form
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse
# from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from EscalArt.forms import FormularioUsuario, editFotoPerfilForm, editPerfilForm, perfilForm, publicacionForm, GuardarPostForm
from .models import Perfil, Publicacion, Usuario, Guardado




# Create your views here.
def ayudacliente(request):
    return render(request,'escalArt/ayudacliente.html')

def delete_publicacion(request,id):
    post = Publicacion.objects.get(idPublicacion=id)
    post.delete()

    return redirect(to='home')

# def delete_guardado(request,id):
#     guardado = Guardado.objects.get(idPublicacion=id)
#     guardado.delete()

#     return redirect(to='home')

def perfil_cliente(request,id):
    user = Usuario.objects.get(username = id)
    list = Perfil.objects.all()
    algo = Perfil.objects.get(idUser = request.user)
    guardados = Guardado.objects.all()
    data = {
        'userInfo':user,
        "perfil":list,
        'foto':editFotoPerfilForm(instance = user),
        'edit': editPerfilForm(instance = algo),
        'guardados':guardados,
    }


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

    post = Publicacion.objects.all()
    list = Perfil.objects.all()
    listArtista = Usuario.objects.all()
    
    # id = request.GET.get('id',None)
    # if id is None:
    #     publi = NULL
    #     print('nothing')
    # else:
    #     print(id)
    #     publi = Publicacion.objects.get(idPublicacion = request.GET.get('id'))
    

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

        }
    else:
        data = {
            "list":artista,

            "posts":post,

            'form':publicacionForm(),
            'perfil':list,
            "listArt":listArtista,

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
                            
                else:
                    
                    print(formulario.errors)
            # print('estas publicando')

            # formulario = publicacionForm(request.POST,request.FILES)           

            # if formulario.is_valid():
            #     publi = formulario.save(commit=False)
            #     publi.idUser = request.user
                    
            #     publi.save()
                            
            # else:
                    
            #     print(formulario.errors)
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
        # elif 'publicacion' in request.POST:
        #     algo = Publicacion.objects.get(idPublicacion = request.POST['idPost'])
            
        #     data = {
        #         "posts":post,

        #         'form':publicacionForm(),
        #         'publi':algo
        #     }
        else:
            print('no se hizo ni un post')
        
    # if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
    #     algo = request.POST.get("idPost")
    #     obj = Publicacion.objects.get(idPublicacion = algo)
    #     data = {
    #         "posts":post,
    #         'form':publicacionForm(),
    #         'publi':obj
    #     }
    #     return render(request, 'escalArt/Perfil_Artista.html',data)
    return render(request, 'escalArt/Perfil_Artista.html',data)

def publicacion(request,artista,post):
    Artista = Usuario.objects.get(username = artista)
    publi = Publicacion.objects.get(idPublicacion = post)

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
                'guardarPost':GuardarPostForm()

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

            }
    else:
        data = {
            "list":Artista,

            "posts":Post,

            'form':publicacionForm(),
            'perfil':list,
            "listArt":listArtista,

            "publi":publi
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

        else:
            ('ningun post ha coincidido')

    else:
        print('no se ha hecho ni un post')
    
    return render(request,'escalArt/publicacion.html',data)


def publicacionHome(request,artista,post):
    Artista = Usuario.objects.get(username = artista)
    publi = Publicacion.objects.get(idPublicacion = post)
    guardados = Guardado.objects.all()
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
                'guardado':guardado              
            }
            
    else:
        data = {
            "list":Artista,

            "posts":Post,

            'form':publicacionForm(),
            'perfil':list,
            "listArt":listArtista,

            "publi":publi
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

        else:
            ('ningun post ha coincidido')
        
    else:
        print('no se ha hecho ni un post')
    return render(request,'escalArt/publicacionHome.html',data)





def home (request):
    list = Perfil.objects.all()
    post = Publicacion.objects.all()
    listArtista = Usuario.objects.all()

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

        "listArt":listArtista

    }
    else:
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        "listArt":listArtista
        
    
    }
    
    # data = {
    #     "perfil":list,
    #     "posts":post,
    #     'form':publicacionForm(),
        
    #     'edit': editPerfilForm(instance = algo)
    # }
    # print(request.user.nombre)
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



# class RegistrarUsuario(CreateView):
#     model = Usuario
#     form_class = FormularioUsuario
#     template_name = 'registration/registro.html'
#     success_url = reverse_lazy('login')

def RegistrarUsuario (request):
    data = {
        "perfil":perfilForm(),
        'form':FormularioUsuario()
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

class AddLike(View):
    def post(self, request, pk, *args, **kwargs):
        post = Publicacion.objects.get(idPublicacion = pk)

        is_liked = False

        for like in post.cantLikes.all():
            if like == request.user:
                is_liked = True
                break
            
        if not is_liked:
            post.cantLikes.add(request.user)

        if is_liked:
            post.cantLikes.remove(request.user)    
        
        next = request.POST.get('next','/')

        return HttpResponseRedirect(next)
        
