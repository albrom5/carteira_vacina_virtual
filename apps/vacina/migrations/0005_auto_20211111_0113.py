# Generated by Django 3.2.8 on 2021-11-11 04:13

import cuser.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacina', '0004_auto_20211109_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doenca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('nome', models.CharField(max_length=50)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_doenca', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_doenca', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FabricanteVacina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('nome', models.CharField(max_length=50)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_fabricantevacina', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_fabricantevacina', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='aplicacao',
            name='lote',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='aplicacao',
            name='vacina',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='aplicacoes_doses', to='vacina.vacina'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vacina',
            name='idade_maxima_aplicacao',
            field=models.PositiveIntegerField(default=999),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vacina',
            name='idade_minima_aplicacao',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aplicacao',
            name='dose',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.DeleteModel(
            name='Dose',
        ),
        migrations.AddField(
            model_name='vacina',
            name='doenca',
            field=models.ManyToManyField(to='vacina.Doenca'),
        ),
        migrations.AddField(
            model_name='vacina',
            name='fabricante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vacina.fabricantevacina'),
        ),
    ]
