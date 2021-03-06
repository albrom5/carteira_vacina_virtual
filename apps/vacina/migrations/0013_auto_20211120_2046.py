# Generated by Django 3.2.8 on 2021-11-20 23:46

from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
        ('vacina', '0012_alter_posto_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacina',
            name='gestante',
            field=models.BooleanField(default=False, verbose_name='Para gestante?'),
        ),
        migrations.AddField(
            model_name='vacina',
            name='sexo',
            field=models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino')], max_length=1),
        ),
        migrations.AlterField(
            model_name='vacina',
            name='idade_maxima_aplicacao',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Idade mínima para aplicação (meses)'),
        ),
        migrations.AlterField(
            model_name='vacina',
            name='idade_minima_aplicacao',
            field=models.PositiveIntegerField(verbose_name='Idade mínima para aplicação (meses)'),
        ),
        migrations.AlterField(
            model_name='vacina',
            name='intervalo_doses',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Intervalo entre as doses (meses)'),
        ),
        migrations.AlterField(
            model_name='vacina',
            name='is_anual',
            field=models.BooleanField(default=False, verbose_name='Dose anual?'),
        ),
    ]
