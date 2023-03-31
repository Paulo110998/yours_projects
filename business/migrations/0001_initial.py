# Generated by Django 4.1 on 2023-03-30 18:25

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
            name='Negocio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=10, null=True, verbose_name='Cliente')),
                ('descriçao', models.CharField(max_length=15, null=True, verbose_name='Descrição do Negócio')),
                ('ticket', models.FloatField(max_length=100, null=True, verbose_name='Ticket do Negócio')),
                ('telefone', models.CharField(max_length=16, null=True, verbose_name='Telefone/Fixo')),
                ('business_partner', models.CharField(max_length=15, null=True, verbose_name='Business Partner')),
                ('commercial_manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Commercial Manager')),
            ],
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contato', models.CharField(choices=[('Feito', 'Contato Feito'), ('Pendente', 'Contato Pedente')], max_length=8, verbose_name='Contato')),
                ('data_contato', models.DateField(auto_now_add=True)),
                ('apresentaçao', models.CharField(choices=[('Feita', 'Apresentação Feita')], max_length=5, verbose_name='Apresentação')),
                ('proposta', models.FileField(upload_to='pdf/')),
                ('status_negociaçao', models.CharField(choices=[('Ativa', 'Negociação Ativa'), ('Inaviva', 'Negociação Inativa'), ('Em Andamento', 'Negociação em Andamento')], max_length=12, verbose_name='Status da Negociação')),
                ('start_negocio', models.CharField(max_length=15, null=True, verbose_name='Start no Negócio')),
                ('negocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.negocio', verbose_name='Negócio/Negociação')),
            ],
        ),
    ]