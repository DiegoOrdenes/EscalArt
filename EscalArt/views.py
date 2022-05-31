from email import message
from tkinter.tix import Form
from django import forms
from django.shortcuts import render,redirect
# from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from EscalArt.forms import FormularioUsuario, editFotoPerfilForm, editPerfilForm, perfilForm, publicacionForm
from .models import Perfil, Publicacion, Usuario

# Create your views here.

def chats(request):
    return render(request, 'escalArt/chats.html')

def presentacion(request):
    return render(request, 'escalArt/presentacion.html')
    
def perfil_cliente_2(request):
    return render(request, 'escalArt/perfil_cliente_2.html')


    

def seleccionarC(request):
    return render(request, 'escalArt/seleccionarC.html')

def ayudacliente(request):
    return render(request,'escalArt/ayudacliente.html')

def perfil_cliente(request):
    return render(request,'escalArt/perfil_cliente.html')

def configuracion(request):
    return render(request,'escalArt/Configuracion.html')
    
def perfil(request):
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
            
            "posts":post,

            'form':publicacionForm(),
            'perfil':list,
            'edit': editPerfilForm(instance = algo),
            'foto': editFotoPerfilForm(instance = user),
            "listArt":listArtista,
            # "publi":publi

        }
    else:
        data = {
            "posts":post,

            'form':publicacionForm(),
            'perfil':list,
            # "publi":publi
        }

    if(request.method=='POST' ):       
        if 'publicar' in request.POST:
            print('estas publicando')
            formulario = publicacionForm(request.POST,request.FILES)           

            if formulario.is_valid():
                obj = formulario.save(commit=False)
                obj.idUser = request.user
                
                obj.save()
                        
            else:
                print('algo paso wn matate')
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
                print('Estas cambiando el header/banner')
                if perfil.is_valid():
                    obj = perfil.save(commit=False)
                    obj.img_header = request.FILES["header"]
                    obj.save()
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

def home (request):
    list = Perfil.objects.all()
    post = Publicacion.objects.all()
    # print(request.user)
    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        
        'edit': editPerfilForm(instance = algo)
    }
    else:
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm()
        
    
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