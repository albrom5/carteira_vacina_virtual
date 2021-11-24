from django.core.management.base import BaseCommand

from apps.vacina.functions import notifica_vacinas_pendentes


class Command(BaseCommand):

    def handle(self, *args, **options):
        notifica_vacinas_pendentes()
