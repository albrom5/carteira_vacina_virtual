# Generated by Django 3.2.8 on 2021-11-11 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacina', '0005_auto_20211111_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacina',
            name='qtd_doses',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]