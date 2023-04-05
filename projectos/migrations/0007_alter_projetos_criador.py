# Generated by Django 4.1 on 2023-04-05 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectos', '0006_alter_cards_criador_alter_projetos_criador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projetos',
            name='criador',
            field=models.ForeignKey(auto_created=True, default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador'),
            preserve_default=False,
        ),
    ]
