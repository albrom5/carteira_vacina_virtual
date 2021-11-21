from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import F

from apps.core.models import BaseModel
from apps.base.models import Usuario

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
    SEXO = (
        ('F', 'Feminino'),
        ('M', 'Masculino')
    )
    nome = models.CharField(max_length=50)
    doenca = models.ManyToManyField(Doenca)
    idade_minima_aplicacao = models.PositiveIntegerField(
        verbose_name='Idade mínima para aplicação (meses)'
    )
    idade_maxima_aplicacao = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='Idade máxima para aplicação (meses)'
    )
    qtd_doses = models.PositiveSmallIntegerField()
    intervalo_doses = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='Intervalo entre as doses (dias)'
    )
    is_anual = models.BooleanField(default=False, verbose_name='Dose anual?')
    para_gestante = models.BooleanField(
        default=False, verbose_name='Gestante pode tomar?'
    )
    gestante_especifica = models.BooleanField(
        default=False, verbose_name='Específica para gestante'
    )
    sexo = models.CharField(max_length=1, choices=SEXO, blank=True)
    fabricante = models.ForeignKey(FabricanteVacina,
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.idade_maxima_aplicacao:
            self.idade_maxima_aplicacao = 9999

        super(Vacina, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        ordering = ['nome']


class Dose(BaseModel):
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    ordem = models.PositiveSmallIntegerField(blank=True)
    proxima_dose = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='Intervalo para a próxima dose (dias)')

    def get_ordem(self):
        doses = Dose.objects.filter(vacina=self.vacina).last()
        if not doses:
            ordem = 1
        else:
            ordem = doses.ordem + 1
        return ordem

    def save(self, *args, **kwargs):
        if not self.ordem:
            self.ordem = self.get_ordem()
        super(Dose, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        Dose.objects.filter(
            vacina=self.vacina, ordem__gt=self.ordem
        ).update(ordem=F('ordem') - 1)
        super(Dose, self).delete(*args, **kwargs)

    def __str__(self):
        return f'{self.vacina} - {self.ordem}'

    class Meta:
        ordering = ['vacina', 'ordem']


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

    def save(self, *args, **kwargs):
        if not self.dose:
            ultima_dose = Aplicacao.objects.filter(
                vacina=self.vacina,
                usuario=self.usuario
            ).order_by('dose').last()
            if ultima_dose:
                self.dose = ultima_dose.dose + 1
            else:
                self.dose = 1
        super(Aplicacao, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.vacina} - {self.data_aplicacao}'

    class Meta:
        verbose_name = 'Aplicação'
        verbose_name_plural = 'Aplicações'
        ordering = ['-data_aplicacao']
