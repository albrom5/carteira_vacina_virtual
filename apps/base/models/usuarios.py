from django.db import models
from django.contrib.auth.models import User

from localflavor.br.models import BRStateField, BRCPFField
from django_countries.fields import CountryField

from apps.base.models import BaseModel, Cidade


class Usuario(BaseModel):
    TIPOS_USUARIOS = (
        ('ADM', 'Administrador'),
        ('PRF', 'Profissional da Saúde'),
        ('CID', 'Cidadão')
    )
    usuario = models.OneToOneField(User, primary_key=True,
                                   on_delete=models.PROTECT)
    tipo = models.CharField(max_length=3, choices=TIPOS_USUARIOS)
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
    descricao = models.CharField(max_length=30)
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

    def save(self, *args, **kwargs):
        if self.principal:
            Endereco.objects.filter(usuario=self.usuario).update(
                principal=False
            )
        super(Endereco, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        if self.principal:
            endereco = Endereco.objects.filter(
                usuario=self.usuario
            ).exclude(id=self.id).order_by('id').first()
            if endereco:
                endereco.principal = True
                endereco.save()
        super(Endereco, self).delete(*args, **kwargs)

    @property
    def endereco_completo(self):
        if self.ender_compl:
            return f'{self.logradouro}, {self.ender_num} {self.ender_compl}' \
                   f' - {self.bairro} - {self.cidade}/{self.estado}'
        else:
            return f'{self.logradouro}, {self.ender_num}' \
                   f' - {self.bairro} - {self.cidade}/{self.estado}'

    def __str__(self):
        return self.endereco_completo


class Telefone(BaseModel):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                related_name='telefones')
    numero = models.CharField(max_length=17)
    principal = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.principal:
            Telefone.objects.filter(usuario=self.usuario).update(
                principal=False
            )
        super(Telefone, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        if self.principal:
            telefone = Telefone.objects.filter(
                usuario=self.usuario
            ).exclude(id=self.id).order_by('id').first()
            if telefone:
                telefone.principal = True
                telefone.save()
        super(Telefone, self).delete(*args, **kwargs)

    def __str__(self):
        return self.numero
