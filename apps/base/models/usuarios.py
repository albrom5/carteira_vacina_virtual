from django.db import models
from django.contrib.auth.models import User

from localflavor.br.models import BRStateField, BRCPFField
from django_countries.fields import CountryField

from apps.base.models import BaseModel, Cidade


class Usuario(BaseModel):
    usuario = models.OneToOneField(User, primary_key=True,
                                   on_delete=models.PROTECT)
    data_nasc = models.DateField(verbose_name='Data de nascimento')
    cpf = BRCPFField(verbose_name='CPF')
    rg = models.CharField(verbose_name='RG', max_length=30, null=True,
                          blank=True)
    org_emis_rg = models.CharField(max_length=200, null=True, blank=True,
                                   verbose_name='Órgão emissor')
    est_emis_rg = BRStateField(null=True, blank=True,
                               verbose_name='Estado emissor')
    nacionalidade = CountryField()
    naturalidade_cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL,
                                            null=True, blank=True,
                                            verbose_name='Natural de')
    naturalidade_estado = BRStateField(null=True, blank=True)

    @property
    def nome_completo(self):
        return f'{self.usuario.first_name} {self.usuario.last_name}'

    def __str__(self):
        return self.nome_completo


class Endereco(BaseModel):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                related_name='enderecos')
    logradouro = models.CharField(verbose_name='Endereço',
                                  max_length=300, null=True, blank=True)
    ender_num = models.CharField(verbose_name='Número',
                                 max_length=30, null=True, blank=True)
    ender_compl = models.CharField(verbose_name='Complemento',
                                   max_length=50, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = BRStateField(null=True, blank=True)
    pais = models.CharField(max_length=100, default='Brasil')
    cep = models.CharField(verbose_name='CEP', max_length=9,
                           null=True, blank=True)
    principal = models.BooleanField(default=True)

    def __str__(self):
        return self.logradouro


class Telefone(BaseModel):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                related_name='telefones')
    numero = models.CharField(max_length=17)
    principal = models.BooleanField(default=True)

    def __str__(self):
        return self.numero
