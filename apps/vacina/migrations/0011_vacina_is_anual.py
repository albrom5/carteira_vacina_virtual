# Generated by Django 3.2.8 on 2021-11-15 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacina', '0010_vacina_intervalo_doses'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacina',
            name='is_anual',
            field=models.BooleanField(default=False),
        ),
    ]