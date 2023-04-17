from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Negocio(models.Model):
    cliente = models.CharField(max_length=20, null=True ,verbose_name='Cliente')
    descriçao = models.CharField(max_length=30, null=True, verbose_name='Descrição do Negócio')
    ticket = models.CharField(max_length=10, null=True, verbose_name='Ticket do Negócio')
    telefone = models.CharField(max_length=16, null=True, verbose_name='Telefone/Fixo') 
    commercial_manager = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Commercial Manager')
    business_partner = models.CharField(max_length=15, null=True, verbose_name='Business Partner')
    data_registro = models.DateField(auto_now_add=True) # Data adicionada automaticamente
    
    def __str__(self):
        return f'{self.cliente} - {self.descriçao} - {self.ticket} - {self.business_partner}'
    

CONTATO = (
    ('Feito', 'Contato Feito'),
    ('Pendente', 'Contato Pedente'),
)

APRESENTAÇAO = (
    ('Feita', 'Apresentação Feita'),
)

STATUS = (
    ('Ativa', 'Negociação Ativa'),
    ('Inaviva', 'Negociação Inativa'),
    ('Em Andamento', 'Negociação em Andamento')
)


class Pipeline(models.Model):
    contato = models.CharField(max_length=8, choices=CONTATO, verbose_name='Contato')
    data_contato = models.DateField(auto_now_add=True)
    apresentaçao = models.CharField(max_length=5, choices=APRESENTAÇAO, verbose_name='Apresentação')
    proposta = models.FileField(upload_to='pdf/')
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, verbose_name='Negócio/Negociação' )
    status_negociaçao = models.CharField(max_length=12, choices=STATUS, verbose_name='Status da Negociação')
    start_negocio = models.CharField(max_length=15, null=True, verbose_name='Start no Negócio')

    def __str__(self):
        return f'{self.contato} - {self.apresentaçao} - {self.status_negociaçao}'




    
    

