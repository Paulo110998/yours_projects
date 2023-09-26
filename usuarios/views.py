from django.shortcuts import render

# Classes de create e update
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
# Autenticação e autenticação por grupos
from django.contrib.auth.models import User, Group
# Formulário personalizado
from .forms import UserCreationForm, Usuarioform
# Listando os dados
from django.urls import reverse_lazy
# Método que busca os grupos de objetos
from django.shortcuts import get_object_or_404
# Importando o model de perfil do usuário
from .models import Perfil

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


# Create your views here.
# CREATEVIEW PARA CADASTRO DE USUÁRIO
class UsuarioCreate(CreateView):
    template_name = 'cadastro_user.html' # Template html
    #classe que criará o registro
    form_class = Usuarioform
    success_url = reverse_lazy('login')
    
    # Validando o cadastro e redirecionando o usuário ao um grupo de acesso
    def  form_valid(self, form):
        #chamando o grupo
        grupo = get_object_or_404(Group, name='Assistants')
        # Validando com o super 
        url = super().form_valid(form)
        #Adicionando o usuario/objeto ao grupo e salvando
        self.object.groups.add(grupo)
        self.object.save()
        
        # Criando um perfil para o usuário que acabou de se cadastrar
        Perfil.objects.create(usuario=self.object)
        return url

def cadastro_concluído(request):
    return render(request, 'cadastro_concluido.html')

def user_list(request):
    users = User.objects.all()
    return render(request,'users_list.html', {'users': users})

#@login_required
#def grupo_users(request):
 #   grupo = request.user.groups.all()[0] # Obtém o primeiro grupo do usuário
  #  contexto = {'grupo': grupo}
   # return render(request, 'users_list.html', contexto)
  

# UPDATE 
class PerfilUpdate(UpdateView, LoginRequiredMixin):
    template_name = 'perfil_update.html' 
    model = Perfil #nova classe
    fields = ['foto_perfil','nome_completo', 'cpf', 'telefone', 'endereço', 'cidade' ,'estado', 'pais']
    success_url = reverse_lazy('perfil-update')

    # Buscando o objeto autenticado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Perfil, usuario=self.request.user) 
        return self.object

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['dados'] = "Meus dados"
        context['botao'] ="Atualizar"

        return context  
    
    

