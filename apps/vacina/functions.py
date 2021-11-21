import datetime

from django.conf import settings
from django.core import mail
from django.db.models import Q
from django.template.loader import render_to_string
from dateutil.relativedelta import relativedelta

from apps.base.models import Usuario
from .models import Vacina, Aplicacao, Dose


def verifica_vacinas(paciente_id):
    """
    Verifica vacinas pendentes
    """

    paciente = Usuario.objects.get(usuario_id=paciente_id)
    if paciente.is_gestante:
        vacinas = Vacina.objects.filter(
            Q(sexo=paciente.sexo) | Q(sexo=''),
            ativo=True,
            idade_minima_aplicacao__lt=paciente.idade_meses,
            idade_maxima_aplicacao__gt=paciente.idade_meses,
            para_gestante=True
        )
    else:
        vacinas = Vacina.objects.filter(
            Q(sexo=paciente.sexo) | Q(sexo=''),
            ativo=True,
            idade_minima_aplicacao__lt=paciente.idade_meses,
            idade_maxima_aplicacao__gt=paciente.idade_meses,
            gestante_especifica=False,
        )

    pendentes = []
    vacina_pendente = {}
    for vacina in vacinas:
        doses_aplicadas = Aplicacao.objects.filter(
            usuario=paciente_id, vacina=vacina).order_by('data_aplicacao')
        doses_necessarias = Dose.objects.filter(
            vacina=vacina).order_by('ordem')
        anual = vacina.is_anual
        if anual or doses_aplicadas.count() < doses_necessarias.count():
            if doses_aplicadas:
                try:
                    proxima_dose = Dose.objects.get(
                        vacina=vacina,
                        ordem=doses_aplicadas.count()
                    ).proxima_dose
                except Dose.DoesNotExist:
                    proxima_dose = vacina.intervalo_doses
                dt_ultima_dose = doses_aplicadas.last().data_aplicacao
                desde_ultima = datetime.date.today() - dt_ultima_dose
                data_prevista = doses_aplicadas.last(
                ).data_aplicacao + relativedelta(days=proxima_dose)
                if proxima_dose <= desde_ultima.days:
                    vacina_pendente['vacina'] = vacina
                    vacina_pendente['doses'] = doses_necessarias.count() - doses_aplicadas.count()
                    vacina_pendente['data_prevista'] = data_prevista
                    pendentes.append(vacina_pendente.copy())
            else:
                vacina_pendente['vacina'] = vacina
                vacina_pendente['doses'] = doses_necessarias.count() - doses_aplicadas.count()
                vacina_pendente['data_prevista'] = datetime.date.today()
                pendentes.append(vacina_pendente.copy())
    return pendentes


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [to])


def notifica_vacinas_pendentes():
    usuarios = Usuario.objects.filter(ativo=True, aceita_email=True)
    for usuario in usuarios:
        vacinas = verifica_vacinas(usuario.usuario_id)
        if vacinas:
            context_email = {'vacinas': vacinas,
                             'paciente': usuario.nome_completo}
            _send_mail('Aviso de vacinação',
                       settings.DEFAULT_FROM_EMAIL,
                       usuario.usuario.email,
                       'vacina/notifica_vacinas_pendentes.txt',
                       context_email)
