# Generated by Django 3.2.8 on 2021-11-21 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacina', '0015_auto_20211120_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacina',
            name='gestante',
        ),
        migrations.AddField(
            model_name='vacina',
            name='gestante_especifica',
            field=models.BooleanField(default=False, verbose_name='Específica para gestante'),
        ),
        migrations.AddField(
            model_name='vacina',
            name='para_gestante',
            field=models.BooleanField(default=False, verbose_name='Gestante pode tomar?'),
        ),
        migrations.AlterField(
            model_name='vacina',
            name='idade_maxima_aplicacao',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Idade máxima para aplicação (meses)'),
        ),
    ]