from django.urls import path

from .views import busca_paciente, visualiza_paciente, RegistraAplicacao

urlpatterns = [
    path('busca_paciente/', busca_paciente, name='busca_paciente'),
    path('visualiza_paciente/<int:paciente_id>/', visualiza_paciente,
         name='visualiza_paciente'),
    path('<int:paciente_id>/registra_aplicacao/', RegistraAplicacao.as_view(),
         name='registra_aplicacao'),
    ]
