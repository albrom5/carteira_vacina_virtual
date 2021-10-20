from django.db import models

from localflavor.br.br_states import STATE_CHOICES


class Cidade(models.Model):
	nome = models.CharField(max_length=60)
	estado = models.CharField(max_length=2, choices=STATE_CHOICES)

	def __str__(self):
		return f'{self.nome}/{self.estado}'

	class Meta:
		ordering = ['estado', 'nome']
