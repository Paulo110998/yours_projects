# Generated by Django 4.1 on 2023-06-13 23:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Projetos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=21, null=True, verbose_name='Título')),
                ('descriçao', models.CharField(max_length=36, null=True, verbose_name='Descrição')),
                ('data_registro', models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 13, 20, 58, 20, 690324))),
                ('criador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador')),
            ],
        ),
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50, null=True, verbose_name='Título')),
                ('descriçao', models.CharField(max_length=100, null=True, verbose_name='Descrição')),
                ('prioridade', models.CharField(choices=[('Baixa', 'Baixa Prioridade'), ('Média', 'Média Prioridade'), ('Alta', 'Alta Prioridade')], max_length=5, verbose_name='Prioridade')),
                ('data_registro', models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 13, 20, 58, 20, 691326))),
                ('criador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador')),
                ('projetos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectos.projetos', verbose_name='Adicionar Projeto')),
            ],
        ),
    ]
