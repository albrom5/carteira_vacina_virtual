import datetime

from django.conf import settings
from django.shortcuts import render, redirect
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from apps.base.functions import identifica_tipo_usuario_logado
from apps.base.models import Usuario
from apps.vacina.forms import RegistraAplicacaoForm
from apps.vacina.functions import _send_mail


def busca_paciente(request):

    if identifica_tipo_usuario_logado(request.user.id) not in ['PRF', 'ADM']:
        return redirect('home')

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

    if identifica_tipo_usuario_logado(request.user.id) not in ['PRF', 'ADM']:
        return redirect('home')

    paciente = Usuario.objects.get(usuario_id=paciente_id)

    return render(request, 'vacina/visualiza_usuario.html',
                  {'paciente': paciente})


class RegistraAplicacao(BSModalCreateView):
    template_name = 'vacina/registra_aplicacao.html'
    success_message = 'Aplicação registrada com sucesso!'
    form_class = RegistraAplicacaoForm

    def get(self, request, *args, **kwargs):
        usuario = Usuario.objects.get(usuario_id=request.user.id)
        form = self.form_class(initial={
            'local': usuario.posto,
            'data_aplicacao': datetime.date.today()
        })
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        aplicacao = form.save(commit=False)
        paciente_id = self.kwargs['paciente_id']
        usuario_logado = Usuario.objects.get(usuario=self.request.user.id)
        aplicacao.usuario = Usuario.objects.get(usuario_id=paciente_id)
        aplicacao.aplicador = usuario_logado
        dest_email = User.objects.get(id=paciente_id)
        context_email = {'aplicacao': form.cleaned_data,
                         'paciente': dest_email.usuario.nome_completo}
        if not self.request.is_ajax():
            # Modal View valida o form 2 vezes, a primeira é Ajax
            _send_mail('Novo registro de vacinação',
                       settings.DEFAULT_FROM_EMAIL,
                       dest_email.email,
                       'vacina/confirmacao_vacina.txt',
                       context_email)
        return super(RegistraAplicacao, self).form_valid(form)

    def get_success_url(self):
        paciente_id = self.kwargs['paciente_id']
        return reverse_lazy('visualiza_paciente',
                            kwargs={'paciente_id': paciente_id})
