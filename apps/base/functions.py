from django.shortcuts import redirect

from .models import Usuario


def identifica_tipo_usuario_logado(user_id):
    try:
        usuario = Usuario.objects.get(usuario_id=user_id)
    except Usuario.DoesNotExist:
        return redirect('custom_login')
    return usuario.tipo
