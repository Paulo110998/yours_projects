# Generated by Django 4.1 on 2023-03-31 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_alter_negocio_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='negocio',
            name='ticket',
            field=models.CharField(max_length=10, null=True, verbose_name='Ticket do Negócio'),
        ),
    ]
