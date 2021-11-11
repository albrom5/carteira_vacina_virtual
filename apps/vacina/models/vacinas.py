from django.db import models

from apps.base.models import BaseModel, Usuario

from .postos import Posto


class Doenca(BaseModel):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class FabricanteVacina(BaseModel):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Vacina(BaseModel):
    nome = models.CharField(max_length=50)
    doenca = models.ManyToManyField(Doenca)
    idade_minima_aplicacao = models.PositiveIntegerField()
    idade_maxima_aplicacao = models.PositiveIntegerField()
    qtd_doses = models.PositiveSmallIntegerField
    fabricante = models.ForeignKey(FabricanteVacina,
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)

    def __str__(self):
        return f'{self.nome} - {self.fabricante}'


class Aplicacao(BaseModel):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT,
                                related_name='aplicacoes')
    vacina = models.ForeignKey(Vacina, on_delete=models.PROTECT,
                               related_name='aplicacoes_doses')
    dose = models.PositiveSmallIntegerField()
    data_aplicacao = models.DateField()
    local = models.ForeignKey(Posto, on_delete=models.PROTECT)
    aplicador = models.ForeignKey(Usuario, on_delete=models.PROTECT,
                                  related_name='aplicadores')
    lote = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.usuario.nome_completo} - {self.dose} - ' \
               f'{self.data_aplicacao}'
