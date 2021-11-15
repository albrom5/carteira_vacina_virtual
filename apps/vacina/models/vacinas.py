from dateutil.relativedelta import relativedelta

from django.db import models

from apps.base.models import BaseModel, Usuario

from .postos import Posto


class Doenca(BaseModel):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Doença'
        verbose_name_plural = 'Doenças'
        ordering = ['nome']


class FabricanteVacina(BaseModel):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'
        ordering = ['nome']


class Vacina(BaseModel):
    nome = models.CharField(max_length=50)
    doenca = models.ManyToManyField(Doenca)
    idade_minima_aplicacao = models.PositiveIntegerField()
    idade_maxima_aplicacao = models.PositiveIntegerField(null=True, blank=True)
    qtd_doses = models.PositiveSmallIntegerField()
    intervalo_doses = models.PositiveSmallIntegerField(null=True, blank=True)
    is_anual = models.BooleanField(default=False)
    fabricante = models.ForeignKey(FabricanteVacina,
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)

    def __str__(self):
        return f'{self.nome} - {self.fabricante}'

    class Meta:
        ordering = ['nome']


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

    @property
    def proxima_dose(self):
        aplicacoes = Aplicacao.objects.filter(usuario_id=self.usuario_id,
                                              vacina=self.vacina)
        if aplicacoes.count() < self.vacina.qtd_doses:
            proxima = self.data_aplicacao + relativedelta(
                months=self.vacina.intervalo_doses
            )
        else:
            proxima = 'Ciclo completo'
        return proxima

    def __str__(self):
        return f'{self.usuario.nome_completo} - {self.vacina} - ' \
               f'{self.data_aplicacao}'

    class Meta:
        verbose_name = 'Aplicação'
        verbose_name_plural = 'Aplicações'
        ordering = ['-data_aplicacao']
