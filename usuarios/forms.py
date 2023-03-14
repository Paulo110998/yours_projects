from django import forms
#Classe de autenticação do django
from django.contrib.auth.models import User  
# Cria o usuário
from django.contrib.auth.forms import UserCreationForm 
# Método que gera um erro se os dados não corresponderem
from django.core.exceptions import ValidationError 

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit


# Criando uma nova view e usando herança do UserCreationForm
class Usuarioform(UserCreationForm):
    #Definindo e-mail padrão
    email = forms.EmailField(max_length=100)

    # Classe para metadados
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    #Método que evita um usuário com o mesmo email (Faz uma limpeza ou vistoria, antes do cadastro ser criado)
    def clean_email(self):
        existente = self.cleaned_data['email'] #Buscando o valor do email validado
        
        # Conferindo se existe um usuário com o mesmo email com o if e else
        if User.objects.filter(email=existente).exists(): # Se o email digitado for igual a 'existente', email que já existe.
            raise ValidationError(f' Este e-mail já existe! Tente outro!')
        else:
            return existente #Se o email não for repetido, cadastro concluído com sucesso!  

    

