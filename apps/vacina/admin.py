from django.contrib import admin

from .models import Vacina, Dose, Aplicacao, Posto, TelefonePosto


admin.site.register(Vacina)

admin.site.register(Aplicacao)

admin.site.register(Dose)

admin.site.register(Posto)

admin.site.register(TelefonePosto)
