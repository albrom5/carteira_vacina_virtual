from django.db import models

from localflavor.br.br_states import STATE_CHOICES


class Cidade(models.Model):
	name = models.CharField(max_length=60)
	state = models.CharField(max_length=2, choices=STATE_CHOICES)

	def __str__(self):
		return f'{self.name}/{self.state}'

	class Meta:
		ordering = ['state', 'name']
