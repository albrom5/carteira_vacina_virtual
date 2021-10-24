# Generated by Django 3.2.8 on 2021-10-24 21:05

import cuser.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.br.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0007_endereco_descricao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('nome', models.CharField(max_length=200)),
                ('logradouro', models.CharField(blank=True, max_length=300, null=True, verbose_name='Endereço')),
                ('ender_num', models.CharField(blank=True, max_length=30, null=True, verbose_name='Número')),
                ('ender_compl', models.CharField(blank=True, max_length=50, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=50, null=True)),
                ('cidade', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', localflavor.br.models.BRStateField(blank=True, max_length=2, null=True)),
                ('pais', models.CharField(default='Brasil', max_length=100)),
                ('cep', models.CharField(blank=True, max_length=9, null=True, verbose_name='CEP')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_posto', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_posto', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vacina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('nome', models.CharField(max_length=50)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_vacina', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_vacina', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TelefonePosto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('numero', models.CharField(max_length=17)),
                ('principal', models.BooleanField(default=True)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_telefoneposto', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('posto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacina.posto')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_telefoneposto', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Aplicacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('data_aplicacao', models.DateField()),
                ('aplicador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='aplicadores', to='base.usuario')),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_aplicacao', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_aplicacao', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vacinados', to='base.usuario')),
                ('vacina', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vacina.vacina')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]