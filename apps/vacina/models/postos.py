from django.db import models

from localflavor.br.models import BRStateField

from apps.base.models import BaseModel


class Posto(BaseModel):
    nome = models.CharField(max_length=200)
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
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nome


class TelefonePosto(BaseModel):
    posto = models.ForeignKey(Posto, on_delete=models.CASCADE)
    numero = models.CharField(max_length=17)
    principal = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.principal:
            TelefonePosto.objects.filter(posto=self.posto).update(
                principal=False
            )
        super(TelefonePosto, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        if self.principal:
            posto = Posto.objects.filter(
                posto=self.posto
            ).exclude(id=self.id).order_by('id').first()
            if posto:
                posto.principal = True
                posto.save()
        super(TelefonePosto, self).delete(*args, **kwargs)

    def __str__(self):
        return self.numero
