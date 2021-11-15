from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from apps.base.models import Endereco, Telefone, Cidade


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


def carrega_cidades(request):
    estado = request.GET.get('estado')
    cidades = Cidade.objects.filter(state=estado).order_by('name')

    return render(
        request, 'base/ajax/cidade_dropdown_list.html', {'cidades': cidades}
    )
