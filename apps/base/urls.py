
from django.urls import path
from .views import (
    home, cadastra_usuario, CustomLoginView, dados_complementares_usuario
)


urlpatterns = [
    path('', home, name='home'),
    path('usuario/novo/', cadastra_usuario, name='novo_usuario'),
    path('dados_adicionais/<int:pk>', dados_complementares_usuario,
         name='complementa_usuario'),
    path('login/', CustomLoginView.as_view(), name='custom_login')
]
