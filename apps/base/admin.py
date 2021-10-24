from django.contrib import admin

from .models import Usuario, Cidade, Telefone

# Register your models here.
admin.site.register(Usuario)

admin.site.register(Cidade)

admin.site.register(Telefone)