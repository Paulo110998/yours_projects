# Generated by Django 4.1 on 2023-03-02 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_welcome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='nome_completo',
            field=models.CharField(max_length=50, null=True, verbose_name='Nome Completo'),
        ),
    ]