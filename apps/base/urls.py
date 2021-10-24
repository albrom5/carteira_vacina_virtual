
from django.urls import path
from .views import (
    home, cadastra_usuario, CustomLoginView, dados_complementares_usuario,
    carrega_cidades, CadastraTelefone
)


urlpatterns = [
    path('', home, name='home'),
    path('usuario/novo/', cadastra_usuario, name='novo_usuario'),
    path('dados_adicionais/<int:pk>', dados_complementares_usuario,
         name='complementa_usuario'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('<int:usuario_id>/cadastra_telefone/', CadastraTelefone.as_view(),
         name='cadastra_telefone'),
    path('ajax/carrega-cidades/', carrega_cidades,
         name='ajax_carrega_cidades'),
]
