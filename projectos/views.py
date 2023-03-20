from django.shortcuts import render
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


# Create your views here.
########## CREATE ##############
# PROJETOS
class ProjetosCreate(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Projetos
    fields = ['titulo', 'descriçao', 'criador']
    template_name = 'criarprojetos.html'
    success_url = reverse_lazy('listar-projetos')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        return url

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
    fields = ['titulo', 'descriçao', 'prioridade', 'membros', 'projetos']
    template_name= "criarcards.html"
    success_url = reverse_lazy('listar-cards') 

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        return url
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['criar_card'] = 'Criar Cards'
        return context
        
###################### UPDATEVIEW ################################

# PROJETOS
class ProjetosUpdate(UpdateView, GroupRequiredMixin, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers']
    model = Projetos
    fields = ['titulo', 'descriçao', 'criador']
    template_name = 'criarprojetos.html'
    success_url = reverse_lazy('listar-projetos')

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['editar_projeto'] = 'Editar Projeto'
        return context

# CARDS
class CardsUpdate(UpdateView, GroupRequiredMixin, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Cards
    fields = ['titulo', 'descriçao', 'prioridade', 'membros']
    template_name = 'criarcards.html'
    success_url = reverse_lazy('listar-cards')

    
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['editar_card'] = 'Editar Card'
        return context

################## DELETEVIEW ###########################
# PROJETOS
class ProjetosDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url ='/login/'     
    redirect_field_name = 'login'
    group_required = [u'Managers']
    models = Projetos
    template_name = 'excluirprojeto.html'
    success_url = reverse_lazy('listar-projetos')  

    
    def get_context_data(self, *args , **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['excluir_projeto'] = 'Excluír Projeto'
        return context
    
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


#################### LISTVIEW #############################
# PROJETOS
class ProjetosList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    models = Projetos
    template_name = 'welcome.html'
    paginate_by = 4
    

    def get_queryset(self):
        self.object_list = Projetos.objects.filter(usuario=self.request.user)
        return self.object_list
    
   # Buscando os objetos(cards) no banco, veja abaixo:
    def get_queryset(self):
        get_projetos = self.request.GET.get('titulo')
        if get_projetos:
            projetos = Projetos.objects.filter(titulo__icontains=get_projetos) 
        else:
            projetos = Projetos.objects.all()
            
        return projetos   

    
   
  
# CARDS
class CardsList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Cards
    template_name = 'cards.html'
    paginate_by = 5


    def get_queryset(self):
        self.object_list = Cards.objects.filter(usuario=self.request.user)
        return self.object_list


    def get_queryset(self):
        get_cards = self.request.GET.get('titulo')
        if get_cards:
            cards = Cards.objects.filter(titulo__icontains=get_cards)
        else:
            cards = Cards.objects.all()
        
        return cards
    
    
    