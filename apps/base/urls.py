
from django.urls import path
from .views import (
    home, cadastra_usuario, CustomLoginView, dados_complementares_usuario,
    carrega_cidades, CadastraTelefone, lista_telefones, TelefoneDeleteView,
    CadastraEndereco, lista_enderecos, EnderecoDeleteView, historico_vacinacao
)


urlpatterns = [
    path('', home, name='home'),
    path('usuario/novo/', cadastra_usuario, name='novo_usuario'),
    path('dados_adicionais/<int:pk>', dados_complementares_usuario,
         name='complementa_usuario'),
    path('historico/', historico_vacinacao, name='historico_vacinacao'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('<int:usuario_id>/cadastra_telefone/', CadastraTelefone.as_view(),
         name='cadastra_telefone'),
    path('apaga_telefone/<int:pk>', TelefoneDeleteView.as_view(),
         name='apaga_telefone'),
    path('ajax/carrega-cidades/', carrega_cidades,
         name='ajax_carrega_cidades'),
    path('<int:usuario_id>/lista_telefones/', lista_telefones,
         name='lista_telefones'),
    path('<int:usuario_id>/cadastra_endereco/', CadastraEndereco.as_view(),
         name='cadastra_endereco'),
    path('apaga_endereco/<int:pk>', EnderecoDeleteView.as_view(),
         name='apaga_endereco'),
    path('<int:usuario_id>/lista_enderecos/', lista_enderecos,
         name='lista_enderecos'),
]
