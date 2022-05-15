from cProfile import label
from dataclasses import field
from socket import fromshare
from tkinter import Widget
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from requests import RequestException, request
from .models import Comision, Comision_Cliente, EstadoComision, Perfil, Publicacion, Referencia, Usuario,Solicitud

# class CustomUserCreationForm(UserCreationForm):
#     pass

#FORMULARIO REGISTRO V

class FormularioUsuario(forms.ModelForm):
    # Formulario de registro de un usuario en la base de datos
    # variables:
    #     -password1: contrasenna
    #     -password2: verificacion de la contrasenna

    password1 = forms.CharField(label = 'Contrasenna',widget = forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Ingrese su contrasenna',
            'id':'password1',
            'required':'required',
        }
    ))
    password2 = forms.CharField(label = 'Contrasenna de confirmacion',widget = forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Confirme contrasenna',
            'id':'password2',
            'required':'required',
        }
    ))


    class Meta:
        model= Usuario
        fields = ('username','email','nombre','tipoCuenta')
        widgets = {
            'username':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su usuario',
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Correo Electronico',
                }
            ),
            'nombre':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su nombre',
                }
            ),
            'tipoCuenta':forms.RadioSelect(
                attrs={
                    'class':'form_radio-input',
                    
                }                
            )

        }
    

    def clean_password2(self):
        #validacion contrasenna
        # 
        #metodo que valida que mabas contrasennas ingresadas sean igual, esto ates
        # de ser encriptadas y guardadas en la base de datos, retornar contrasenna valida
        # 
        # excepciones: validationError -- cuando las contrasennas no son iguales muestra un mensaje de error

        password1 = self.cleaned_data.get('password1') 
        password2 = self.cleaned_data.get('password2') 

        if password1 != password2:
            raise forms.ValidationError('Contrasennas no coinciden!')
        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

# class PerfilForm(forms.ModelForm):
#     class Meta:
#         model = Perfil
#         fields = ['seguidos','seguidores','calificacion','biografia','idUser']


class publicacionForm( ModelForm):
    cantLikes = forms.IntegerField(initial=0)
    
    
    
    class Meta:
        model=Publicacion
        fields = ['descripcion','titulo','imagen','cantLikes']
        exclude = ['idUser','imagen']
        widgets = {
            'titulo':forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese un titulo',
                    'id':'titulo-post'
                
                }
            ),
            'descripcion':forms.Textarea(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingresa una descripcion',
                    'id':'descripcion-post',
                    
                }
            )
        }


class perfilForm(ModelForm):
    seguidos = forms.IntegerField(initial = 0)
    seguidores = forms.IntegerField(initial = 0)
    calificacion = forms.IntegerField(initial = 0)
   

    class Meta:
        model = Perfil
        fields = ['seguidos','seguidores','calificacion','idUser']
        exclude = ['idUser','biografia','img_header']

class editPerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['biografia','img_header']
        widgets = {
            'biografia':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese biografia'
                }
            )

        }

class editFotoPerfilForm(ModelForm):
    class Meta:
        model = Usuario
        fields=['imagen']
        # widgets = {
        #     'imagen': forms.FileInput(),
        # }
        exclude = ['idUser','username','email','nombre','tipoCuenta','usuario_activo','usuario_administrador','objects']
    
class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['idCliente','usernameArtista','idSolicitud']
        exclude = ['idCliente','usernameArtista','idSolicitud']
        
class ComisionArtistaForm(ModelForm):    

    class Meta:
        model = Comision
        fields = ['idEstado','idArtista']
        exclude = ['idEstado','idArtista']

class EditComArtForm(ModelForm):
    class Meta:
        model = Comision
        fields = ['idEstado','idArtista']
        exclude = ['idArtista']

class ComisionClienteForm(ModelForm):
    class Meta:
        model = Comision_Cliente
        fields = ['idComision','idCliente']
        exclude = ['idComision','idCliente']

class ReferenciasForm(ModelForm):
    class Meta:
        model = Referencia
        fields = ['img_referencia','idUser','usernameArtista']
        exclude = ['idUser','usernameArtista']


         