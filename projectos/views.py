
# Views de Crud e Lis
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
# Views de Autenticação
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.auth.models import User
# Configura uma página de erro mais bonita e clean
from django.shortcuts import get_object_or_404 
# Importando models dos projectos
from .models import Projetos, Cards
from django.urls import reverse_lazy
# Importando módulo para gerar csv
import csv
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
########## CREATE ##############
# PROJETOS
class ProjetosCreate(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    login_url = '/login/' # Só acessa a pagina se tiver logado
    redirect_field_name = 'login' # Redireciona para o login
    group_required = [u'Managers', u'Assistants'] # Acesso restrito por grupos
    model = Projetos # Model
    fields = ['titulo', 'descriçao', 'criador'] # Adiciono os campos de cadastros que devem aparecer
    template_name = 'criarprojetos.html' # Template
    success_url = reverse_lazy('welcome') # Lista os dados após o create
    
    
    #Método que valida os dados do create 
    def form_valid(self, form):
        # Antes do super não é criado o objeto nem salvo no banco
        form.instance.usuario = self.request.user
       
        # form.instance -> Pegando a instância do obj no momento do cadastro
        # usuario -> coluna do model
        # self.request.user -> Buscando o usuário que fez a requisição da classe
        
        # Depois do super o objeto é criado
        url = super().form_valid(form)
        messages.success(self.request,"Projeto criado com sucesso!")
        return url
    
   
   # Método que torna possível o envio de dados para o template, ou seja podemos usar o mesmo template para create e update, através da view
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['criar_pj'] = 'Criar projeto'
        return context
    
    

# CARDS
class CardsCreate(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Cards
    fields = ['titulo', 'descriçao', 'prioridade', 'projetos', 'criador']
    template_name= "criarcards.html"
    success_url = reverse_lazy('listar-cards') 
    


    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, "Lista criada com sucesso!") # Mensagem que deve aparecer no template
        return url
  
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['criar_lista'] = 'Criar Lista'
        return context
    
    
###################### UPDATEVIEW ################################
# PROJETOS
class ProjetosUpdate(UpdateView, GroupRequiredMixin, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers']
    model = Projetos
    fields = ['titulo', 'descriçao', 'criador']
    template_name = 'updateprojeto.html'
    success_url = reverse_lazy('welcome')

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['editar_projeto'] = 'Editar Projeto'
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, "Projeto atualizado!") # Mensagem que deve aparecer no template
        return url

# CARDS
class CardsUpdate(UpdateView, GroupRequiredMixin, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Cards
    fields = ['titulo', 'descriçao', 'prioridade', 'projetos']
    template_name = 'updatecard.html'
    success_url = reverse_lazy('listar-cards')

    
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['editar_lista'] = 'Editar Lista'
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, "Lista atualizada!") # Mensagem que deve aparecer no template
        return url

################## DELETEVIEW ###########################
# PROJETOS
class ProjetosDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url ='/login/'     
    redirect_field_name = 'login'
    group_required = [u'Managers']
    models = Projetos
    template_name = 'excluirprojeto.html'
    success_url = reverse_lazy('welcome')  

    
    def get_context_data(self, *args , **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['excluir_projeto'] = 'Excluír Projeto'
        return context
    
    def form_valid(self, form):
        url = super().form_valid(form)
        messages.success(self.request,"Projeto Excluído!")
        return url

# CARDS
class CardsDelete(DeleteView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Cards
    template_name = "excluircards.html"
    success_url = reverse_lazy('listar-cards')

    def get_context_data(self, *args , **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['excluir_cards'] = 'Excluír Card'
        return context
    
    def form_valid(self, form):
        url = super().form_valid(form)
        messages.success(self.request,"Lista Excluída!")
        return url


#################### LISTVIEW #############################
# PROJETOS
class ProjetosList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    models = Projetos
    template_name = 'welcome.html'
    paginate_by = 4
    ordering = ['titulo'] # Ordenando a listagem de objetos
    
    
    def get_queryset(self):
        self.object_list = Projetos.objects.filter(usuario=self.request.user)
        return self.object_list
    
   # Buscando os objetos(cards) no banco, veja abaixo:
    def get_queryset(self):
        get_projetos = self.request.GET.get('titulo') # Buscando o título do objeto no servidor/banco de dados
        if get_projetos:
            projetos = Projetos.objects.filter(titulo__icontains=get_projetos).order_by('id') # Filtrando o título e ordenando através do id
        else:
            projetos = Projetos.objects.all().order_by('titulo') # Listando todos objetos 
            
        return projetos   

    
# CARDS
class CardsList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Cards
    template_name = 'cards.html'
    paginate_by = 5
    ordering = ['titulo'] # Ordenando a listagem por 'titulo'

    
    # Método que por padrão lista todos os objetos criados
    def get_queryset(self):
        get_cards = self.request.GET.get('titulo')
        if get_cards:
            cards = Cards.objects.filter(titulo__icontains=get_cards)
        else:
            cards = Cards.objects.all().order_by('titulo') # Ordenando a listagem dos objetos
        
        return cards
    
    
    






    # Exportando dados em csv
    def export_csv(request, self):
        
        response = HttpResponse(
            content_type = 'text/csv',
            headers={'Content-Disposition': 'attachment; filename="mylists.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(Cards.objects.all(['titulo', 'descriçao', 'prioridade', 'criador', 'projetos']))
        writer.save()
        return response
    
    
    