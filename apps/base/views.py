from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView
from django.template.loader import render_to_string
from django.urls import reverse_lazy


from .models import Usuario, Cidade, Telefone, Endereco
from .forms import (
    NovoUsuarioForm, CustomLoginForm, DadosComplementaresUsuarioForm,
    TelefoneForm, EnderecoForm
)
from apps.vacina.models import Aplicacao


def home(request):
    context = {}
    if request.user.is_authenticated:
        context['usuario'] = request.user
        aplicacoes = Aplicacao.objects.filter(usuario=request.user.id)
        context['aplicacoes'] = aplicacoes

        return render(request, 'base/index.html', context)
    else:
        return redirect('custom_login')


def cadastra_usuario(request):
    context = {}
    template = 'base/novo_usuario.html'

    if request.method == 'POST':
        form = NovoUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            primeiro_nome = form.cleaned_data.get('primeiro_nome')
            sobrenome = form.cleaned_data.get('sobrenome')
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('password2')
            cpf = form.cleaned_data.get('cpf')
            usuario.usuario = User.objects.create_user(
                username=cpf, email=email, password=senha,
                first_name=primeiro_nome, last_name=sobrenome
            )
            form.save()
            id_usuario = User.objects.get(username=cpf)
            new_user = authenticate(username=form.cleaned_data['cpf'],
                                    password=form.cleaned_data['password2'],
                                    )
            login(request, new_user)
            return redirect('complementa_usuario', id_usuario.id)
    else:
        form = NovoUsuarioForm()

    context['form'] = form
    return render(request, template, context)

def dados_complementares_usuario(request, pk):
    context = {}
    template = 'base/complementa_usuario.html'
    usuario = Usuario.objects.get(usuario_id=pk)
    context['object'] = usuario
    if request.user.is_authenticated and request.user.id == pk:
        if request.method == 'POST':
            form = DadosComplementaresUsuarioForm(request.POST,
                                                  instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DadosComplementaresUsuarioForm(instance=usuario,
                                                  initial={
                                                      'nacionalidade': 'BR'
                                                  })
        telefones = Telefone.objects.filter(usuario=usuario)
        enderecos = Endereco.objects.filter(usuario=usuario)
        context['form'] = form
        context['telefones'] = telefones
        context['enderecos'] = enderecos
        return render(request, template, context)
    else:
        return redirect('custom_login')


class CustomLoginView(LoginView):
    form_class = CustomLoginForm


def carrega_cidades(request):
    estado = request.GET.get('estado')
    cidades = Cidade.objects.filter(state=estado).order_by('name')

    return render(
        request, 'base/ajax/cidade_dropdown_list.html', {'cidades': cidades}
    )


class CadastraTelefone(BSModalCreateView):
    template_name = 'base/cadastra_telefone.html'
    form_class = TelefoneForm
    success_message = 'Telefone cadastrado'

    def form_valid(self, form):
        telefone = form.save(commit=False)
        usuario_id = self.kwargs['usuario_id']
        usuario = Usuario.objects.get(usuario_id=usuario_id)
        telefone.usuario = usuario
        return super(CadastraTelefone, self).form_valid(form)

    def get_success_url(self):
        usuario_id = self.kwargs['usuario_id']
        return reverse_lazy('complementa_usuario', kwargs={'pk': usuario_id})


class TelefoneDeleteView(BSModalDeleteView):
    model = Telefone
    template_name = 'base/apaga_telefone.html'
    success_message = 'Telefone apagado'

    def get_success_url(self):
        usuario_id = self.object.usuario.usuario_id
        return reverse_lazy('complementa_usuario', kwargs={'pk': usuario_id})


def lista_telefones(request, usuario_id):
    data = dict()

    if request.method == 'GET':
        telefones_usuario = Telefone.objects.filter(usuario_id=usuario_id)
        # asyncSettings.dataKey = 'table'
        data['table'] = render_to_string(
            'base/_telefones_table.html',
            {'telefones': telefones_usuario},
            request=request
        )
        return JsonResponse(data)


class CadastraEndereco(BSModalCreateView):
    template_name = 'base/cadastra_endereco.html'
    form_class = EnderecoForm
    success_message = 'Endereço cadastrado'

    def form_valid(self, form):
        endereco = form.save(commit=False)
        usuario_id = self.kwargs['usuario_id']
        usuario = Usuario.objects.get(usuario_id=usuario_id)
        endereco.usuario = usuario
        return super(CadastraEndereco, self).form_valid(form)

    def get_success_url(self):
        usuario_id = self.kwargs['usuario_id']
        return reverse_lazy('complementa_usuario', kwargs={'pk': usuario_id})


class EnderecoDeleteView(BSModalDeleteView):
    model = Endereco
    template_name = 'base/apaga_endereco.html'
    success_message = 'Endereço apagado'

    def get_success_url(self):
        usuario_id = self.object.usuario.usuario_id
        return reverse_lazy('complementa_usuario', kwargs={'pk': usuario_id})


def lista_enderecos(request, usuario_id):
    data = dict()

    if request.method == 'GET':
        enderecos_usuario = Endereco.objects.filter(usuario_id=usuario_id)
        # asyncSettings.dataKey = 'table'
        data['table'] = render_to_string(
            'base/_enderecos_table.html',
            {'enderecos': enderecos_usuario},
            request=request
        )
        return JsonResponse(data)
