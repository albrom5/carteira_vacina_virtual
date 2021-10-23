from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from .models import Usuario
from .forms import (
    NovoUsuarioForm, CustomLoginForm, DadosComplementaresUsuarioForm
)

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['usuario'] = request.user
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
    if request.method == 'POST':
        form = DadosComplementaresUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():

            return redirect('custom_login')
    else:
        form = DadosComplementaresUsuarioForm(instance=usuario)

    context['form'] = form
    return render(request, template, context)


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
