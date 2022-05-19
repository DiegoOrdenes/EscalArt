from email import message
from tkinter.tix import Form
from django import forms
from django.shortcuts import render,redirect
# from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from EscalArt.forms import ComisionArtistaForm, ComisionClienteForm, EditComArtForm, FormularioUsuario, ReferenciasForm, editFotoPerfilForm, editPerfilForm, perfilForm, publicacionForm,SolicitudForm
from .models import Comision, Comision_Cliente, EstadoComision, Perfil, Publicacion, Referencia, Solicitud, Usuario

# Create your views here.
def home (request):
    list = Perfil.objects.all()
    post = Publicacion.objects.all()
    comisionCli = Comision_Cliente.objects.all()
    comisionArt = Comision.objects.all()
    listArtista = Usuario.objects.all()
    # print(request.user)
    if (request.user.is_authenticated):
        # print(comisionArt.values('idComision').filter(idArtista = request.user))

        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        
        'edit': editPerfilForm(instance = algo),
        'foto':editFotoPerfilForm(instance = user),
        "comCli":comisionCli,
        "comArt":comisionArt,
        "listArt":listArtista
    }
    else:
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        "listArt":listArtista        
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

def delete_publicacion(request,id):
    post = Publicacion.objects.get(idPublicacion=id)
    post.delete()

    return redirect(to='home')

def delete_comision(request,id):
    comision = Comision.objects.get(idComision = id)
    comision.delete()
    
    return redirect(to='home')

def perfilArtista(request,id):
    artista = Usuario.objects.get(username = id)
    post = Publicacion.objects.all()


    data ={
        'list': artista,
        "posts":post,
        'form': SolicitudForm(),

    }
    if (request.method == 'POST' and 'solicitud' in request.POST):
        form = SolicitudForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit = False)
            obj.idSolicitud = f"{request.user}-{artista.username}"
            obj.idCliente = request.user
            obj.usernameArtista = artista.username
            obj.save()
            # return render(request,'escalArt/mensajes.html',data)
        else:
            print(form.errors)
    else:
        print('no esta entrando')

    return render(request,'escalArt/perfilArtista.html',data)

def mensajes(request,id):
    artista = Usuario.objects.get(username = id)
    cliente = Usuario.objects.all()
    estadoCom = EstadoComision.objects.get(idEstado = 1)
    algo = Solicitud.objects.all()
    referencias = Referencia.objects.all()
    data ={
        'list': artista,
        'sol':algo,
        'cli':cliente,
        'comArt':ComisionArtistaForm,
        'comCli':ComisionClienteForm,
        'ref':ReferenciasForm(),
        'refAll': referencias

    }
    if(request.method=='POST' ):
        if 'comision' in request.POST:
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
        elif 'referencia' in request.POST:
            print('estas subiendo una referencia')
            referencia = ReferenciasForm(request.POST,request.FILES)
            

            if referencia.is_valid():
                ref = referencia.save(commit=False)
                ref.usernameArtista = request.POST['ref']
                ref.idUser = request.user
                
                ref.save()
                        
            else:
                print('algo paso wn matate')
                print(referencia.errors)
            

        else:
            print('no esta entrando')
    return render(request,'escalArt/mensajes.html',data)

def PerfilCliente(request,id):
   
    comCli = Comision_Cliente.objects.filter(idCliente = id)
    cliente = Usuario.objects.get(idUser = id)
    

    # comArt = Comision.objects.get()
    data ={
        'comCli':comCli,
        'Cli':cliente,
        # 'comArt':comArt,
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
    

    return render(request,'escalArt/perfilCliente.html',data)



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