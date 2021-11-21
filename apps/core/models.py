from django.db import models
from cuser.fields import CurrentUserField


# Modelo padrão contendo os campos comuns a todas os models do sistema
class BaseModel(models.Model):
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField('Incluído em:', auto_now_add=True,
                                     editable=False, null=True)
    criador = CurrentUserField(verbose_name='Incluído por:', add_only=True,
                               on_delete=models.SET_NULL,
                               related_name="created_%(class)s")
    modificado_em = models.DateTimeField('Alterado em:', auto_now=True,
                                         null=True)
    ultimo_editor = CurrentUserField(verbose_name='Alterado por:',
                                     on_delete=models.SET_NULL,
                                     related_name="last_edited_%(class)s")

    class Meta:
        abstract = True  # Set this model as Abstract
