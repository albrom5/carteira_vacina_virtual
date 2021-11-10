from django.db import models

from apps.base.models import BaseModel, Usuario

from .postos import Posto

class Vacina(BaseModel):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Dose(BaseModel):
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE,
                               related_name='doses')
    ordem = models.IntegerField()
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.vacina} - {self.ordem}ª dose'


class Aplicacao(BaseModel):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT,
                                related_name='aplicacoes')
    dose = models.ForeignKey(Dose, on_delete=models.PROTECT,
                             related_name='aplicacoes_doses')
    data_aplicacao = models.DateField()
    local = models.ForeignKey(Posto, on_delete=models.PROTECT)
    aplicador = models.ForeignKey(Usuario, on_delete=models.PROTECT,
                                  related_name='aplicadores')

    def __str__(self):
        return f'{self.usuario.nome_completo} - {self.dose} - ' \
               f'{self.data_aplicacao}'
