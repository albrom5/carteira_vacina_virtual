from django.shortcuts import render
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy

from apps.base.models import Usuario
from .forms import RegistraAplicacaoForm

def busca_paciente(request):
    filtro_cpf = request.GET.get('cpf')
    context = {}
    if filtro_cpf:
        try:
            paciente = Usuario.objects.get(cpf=filtro_cpf)
        except Usuario.DoesNotExist:
            context['erro'] = 'CPF não encontrado'
            paciente = None
    else:
        paciente = None
    context['paciente'] = paciente

    return render(request, 'vacina/busca_usuario.html', context)


def visualiza_paciente(request, paciente_id):

    paciente = Usuario.objects.get(usuario_id=paciente_id)

    return render(request, 'vacina/visualiza_usuario.html',
                  {'paciente': paciente})


class RegistraAplicacao(BSModalCreateView):
    template_name = 'vacina/registra_aplicacao.html'
    success_message = 'Aplicação registrada com sucesso!'
    form_class = RegistraAplicacaoForm

    def form_valid(self, form):
        aplicacao = form.save(commit=False)
        paciente_id = self.kwargs['paciente_id']
        usuario_logado = Usuario.objects.get(usuario=self.request.user.id)
        aplicacao.usuario = Usuario.objects.get(usuario_id=paciente_id)
        aplicacao.aplicador = usuario_logado
        return super(RegistraAplicacao, self).form_valid(form)

    def get_success_url(self):
        paciente_id = self.kwargs['paciente_id']
        return reverse_lazy('visualiza_paciente', kwargs={'paciente_id': paciente_id})
