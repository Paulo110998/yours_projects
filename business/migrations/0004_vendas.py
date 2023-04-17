# Generated by Django 4.1 on 2023-04-17 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0003_alter_negocio_descriçao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Em Andamento', 'Venda em Andamento'), ('Concluido', 'Venda Concluída')], max_length=12, verbose_name='Business Status')),
                ('commercial_manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Commercial Manager')),
                ('nome_do_negocio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='business.negocio')),
            ],
        ),
    ]
