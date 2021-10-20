from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from .forms import NovoUsuarioForm


def home(request):
    context = {}
    if request.user.is_authenticated:
        context['usuario'] = request.user
        return render(request, 'base/index.html', context)
    else:
        return redirect('login')


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
            senha = form.cleaned_data.get('senha')
            usuario.usuario = User.objects.create_user(
                username=email, email=email, password=senha,
                first_name=primeiro_nome, last_name=sobrenome
            )
            form.save()
            return redirect('login')
    else:
        form = NovoUsuarioForm()

    context['form'] = form
    return render(request, template, context)
