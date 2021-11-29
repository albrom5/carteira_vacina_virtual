# Generated by Django 3.2.8 on 2021-11-21 00:15

import cuser.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacina', '0013_auto_20211120_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('vacina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             to='vacina.vacina')),
                ('ordem', models.PositiveSmallIntegerField()),
                ('proxima_dose',
                 models.PositiveSmallIntegerField(blank=True, null=True,
                                                  verbose_name='Intervalo para a próxima dose (meses)')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em',
                 models.DateTimeField(auto_now_add=True, null=True,
                                      verbose_name='Incluído em:')),
                ('modificado_em',
                 models.DateTimeField(auto_now=True, null=True,
                                      verbose_name='Alterado em:')),
                ('criador',
                 cuser.fields.CurrentUserField(editable=False, null=True,
                                               on_delete=django.db.models.deletion.SET_NULL,
                                               related_name='created_aplicacao',
                                               to=settings.AUTH_USER_MODEL,
                                               verbose_name='Incluído por:')),
                ('ultimo_editor',
                 cuser.fields.CurrentUserField(editable=False, null=True,
                                               on_delete=django.db.models.deletion.SET_NULL,
                                               related_name='last_edited_aplicacao',
                                               to=settings.AUTH_USER_MODEL,
                                               verbose_name='Alterado por:')),
            ],
            options={
                'ordering': ['vacina', 'ordem'],
                'abstract': False,
            },
        ),
    ]