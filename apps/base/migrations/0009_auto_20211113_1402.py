# Generated by Django 3.2.8 on 2021-11-13 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_usuario_tipo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='endereco',
            options={'ordering': ['usuario', 'id'], 'verbose_name': 'Endereço', 'verbose_name_plural': 'Endereços'},
        ),
        migrations.AlterModelOptions(
            name='telefone',
            options={'ordering': ['usuario', 'id']},
        ),
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ['tipo', 'usuario'], 'verbose_name': 'Usuário', 'verbose_name_plural': 'Usuários'},
        ),
    ]
