# Generated by Django 3.2.8 on 2021-11-13 21:11

import cuser.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacina', '0007_auto_20211113_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoordenadasPosto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('latitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_coordenadasposto', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('posto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacina.posto')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_coordenadasposto', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
