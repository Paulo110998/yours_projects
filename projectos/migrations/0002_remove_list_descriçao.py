# Generated by Django 4.0.5 on 2023-09-21 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='descriçao',
        ),
    ]
