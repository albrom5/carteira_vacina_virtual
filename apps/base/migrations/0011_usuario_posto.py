# Generated by Django 3.2.8 on 2021-11-21 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacina', '0017_auto_20211121_0037'),
        ('base', '0010_auto_20211113_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='posto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vacina.posto'),
        ),
    ]
