import datetime
from django.core import mail
from django.template.loader import render_to_string
from dateutil.relativedelta import relativedelta

from apps.base.models import Usuario
from .models import Vacina, Aplicacao


def verifica_vacinas(paciente_id):
    """
    Verifica vacinas pendentes
    """
    vacinas = Vacina.objects.filter(ativo=True)

    paciente = Usuario.objects.get(usuario_id=paciente_id)

    pendentes = []
    vacina_pendente = {}
    for vacina in vacinas:
        doses_aplicadas = Aplicacao.objects.filter(usuario=paciente_id,
                                                   vacina=vacina)
        if vacina.is_anual:
            ultima_dose = datetime.date.today() - doses_aplicadas.first().data_aplicacao
            if ultima_dose.days > 366:
                data_prevista = doses_aplicadas.last().data_aplicacao + relativedelta(months=12)
                vacina_pendente['vacina'] = vacina
                vacina_pendente['data_prevista'] = data_prevista
                pendentes.append(vacina_pendente.copy())
        elif doses_aplicadas.count() < vacina.qtd_doses:
            diferenca = vacina.qtd_doses - doses_aplicadas.count()
            vacina_pendente['vacina'] = vacina
            vacina_pendente['diferenca'] = diferenca
            pendentes.append(vacina_pendente.copy())
    return pendentes


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [to])
