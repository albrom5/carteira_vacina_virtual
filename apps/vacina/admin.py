from django.contrib import admin

from .models import Vacina, Aplicacao, Posto, TelefonePosto


admin.site.register(Vacina)

admin.site.register(Aplicacao)

admin.site.register(Posto)

admin.site.register(TelefonePosto)
