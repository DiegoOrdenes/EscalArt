from django.contrib import admin
from .models import Comentarios, Guardado, Perfil, Publicacion,  Referencia, TipoCuenta, Usuario, Comision,Comision_Cliente,EstadoComision
from .models import Solicitud
# Register your models here.


# admin.site.register(Categoria)
admin.site.register(TipoCuenta)
admin.site.register(Usuario)
admin.site.register(Publicacion)
admin.site.register(Perfil)
# admin.site.register(Publicacion_Categoria)
# admin.site.register(Usuario_Categoria)
admin.site.register(Comentarios)
admin.site.register(Comision)
admin.site.register(Comision_Cliente)
admin.site.register(EstadoComision)
admin.site.register(Solicitud)
admin.site.register(Referencia)
admin.site.register(Guardado)




