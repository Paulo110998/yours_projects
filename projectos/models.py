from django.db import models
from distutils.command.upload import upload
from tabnanny import verbose
from django.contrib.auth.models import User



# Create your models here.
class Projetos(models.Model):
    titulo = models.CharField(max_length=70, null=True, verbose_name='Título')
    descriçao = models.CharField(max_length=100, null=True, verbose_name='Descrição')
    criador = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Membros do Projeto")


    def __str__(self):
        return f'{self.titulo} - {self.descriçao} - {self.criador}'


PRIORIDADE_CARDS = (
    ('Baixa', 'Baixa Prioridade'),
    ('Média', 'Média Prioridade'),
    ('Alta', 'Alta Prioridade'),
)


class Cards(models.Model):
    titulo = models.CharField(max_length=50, null=True, verbose_name="Título")
    descriçao = models.CharField(max_length=100, null=True, verbose_name="Descrição")
    prioridade = models.CharField(max_length=5, choices=PRIORIDADE_CARDS , verbose_name = 'Prioridade')
    membros = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Membros")

    def __str__(self):
        return f'{self.titulo} - {self.descriçao} - {self.prioridade} - {self.membros}'
    
    

    