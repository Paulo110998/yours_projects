from django.db import models
from distutils.command.upload import upload
from tabnanny import verbose
from turtle import width
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    nome_completo = models.CharField(max_length=50, null=True, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=17, null=True, verbose_name='CPF')
    telefone = models.CharField(max_length=16, null=True)
    endereço = models.CharField(max_length=150, null=True)
    cidade = models.CharField(max_length=50, null=True)
    estado = models.CharField(max_length=20, null=True)
    pais = models.CharField(max_length=20,null=True, verbose_name='País')
    foto_perfil = models.ImageField(upload_to="img/",height_field=None, width_field=None, max_length=100, null=True, blank=True, verbose_name='Foto de Perfil')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) #OneToOneField -> Um usuário só pode ter um perfil
