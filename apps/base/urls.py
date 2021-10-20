
from django.urls import path
from .views import home, cadastra_usuario

urlpatterns = [
    path('', home, name='home'),
    path('usuario/novo/', cadastra_usuario, name='novo_usuario')
]
