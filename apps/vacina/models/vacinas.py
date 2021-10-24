from django.db import models

from apps.base.models import BaseModel, Usuario

from .postos import Posto

class Vacina(BaseModel):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Aplicacao(BaseModel):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT,
                                related_name='vacinados')
    vacina = models.ForeignKey(Vacina, on_delete=models.PROTECT)
    data_aplicacao = models.DateField()
    local = models.ForeignKey(Posto, on_delete=models.PROTECT)
    aplicador = models.ForeignKey(Usuario, on_delete=models.PROTECT,
                                  related_name='aplicadores')

    def __str__(self):
        return f'{self.usuario.nome_completo} - {self.vacina} - ' \
               f'{self.data_aplicacao}'
