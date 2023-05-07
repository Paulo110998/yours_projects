from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Negocio, Pipeline
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Sum

# Create your views here.
############### CREATE ##################
class CreateNegocio(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Negocio
    fields = ['cliente', 'descriçao', 'ticket', 'telefone', 'commercial_manager', 'business_partner']
    template_name = 'criar_negocio.html'
    success_url = reverse_lazy('your-business')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, "Negócio criado!")
        return url
    
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['criar_negocio'] = 'Adicionar Negócio'
        return context


class CreatePipeline(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url ='/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Pipeline
    fields = ['contato', 'data_contato', 'apresentaçao', 'proposta', 'negocio', 'status_negociaçao', 'start_negocio']
    template_name = 'criar_pipeline.html'
    success_url = reverse_lazy('pipeline')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, "Pipeline Criado!")
        return url
    
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['criar_pipeline'] = 'Criar Pipeline'
        return context



################ UPDATE #####################
class UpdateNegocio(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Negocio
    fields = ['cliente', 'descriçao', 'ticket', 'telefone', 'commercial_manager', 'business_partner']
    template_name = 'updatenegocio.html'
    success_url = reverse_lazy('your-business')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, "Negócio atualizado!")
        return url

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['editar_negocio'] = 'Editar Negócio'
        return context


class UpdatePipeline(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    login_url ='/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Pipeline
    fields = ['contato', 'data_contato', 'apresentaçao', 'proposta', 'negocio', 'status_negociaçao', 'start_negocio']
    template_name = 'criar_pipeline.html'
    success_url = reverse_lazy('pipeline')

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['editar_pipeline'] = 'Editar Pipeline'
        return context
    
    
################## DELETEVIEW ##################
class DeleteNegocio(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Negocio
    template_name = 'deletar_negocio.html'
    success_url = reverse_lazy('your-business')
    
    def form_valid(self, form):
        url = super().form_valid(form)
        messages.success(self.request, "Negócio excluido!")
        return url
    
    
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['deletar_negocio'] = 'Excluir Negócio'
        return context
    
    
class DeletePipeline(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Pipeline
    template_name = 'deletar_pipeline.html'
    success_url = reverse_lazy('pipeline')

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['deletar_pipeline'] = 'Excluir Pipeline'
        return context


################# LISTVIEW #####################
class NegocioList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Negocio
    template_name = 'business.html'
    paginate_by = 4
    ordering = ['cliente']
    
    
    def get_queryset(self):
        get_negocio = self.request.GET.get('cliente')
        if get_negocio:
            negocio = Negocio.objects.filter(cliente__icontains=get_negocio)
        else:
            negocio = Negocio.objects.all().order_by('cliente')
        return negocio


# values_list() -> é uma otimização para obter dados específicos do banco de dados
# flat=true -> Apenas retornará valores únicos, em vez de tuplas.
# distinct() ->  Garante que os resultados sejam filtrados e retornados corretamente, remove quaisquer resultados duplicados.
def quantidade_negocio(request):
    negocios = Negocio.objects.values_list('ticket', flat=True).distinct() 
    contagens = {}
    for ticket in negocios:
        contagens[ticket] = Negocio.objects.filter(ticket=ticket).count() # Buscando a quantidade de tickets 
    return render(request, 'chart.html',  {'contagens': contagens})

# Relatório de clientes
def Negocios(request):
    relatorio = Negocio.objects.all()
    return render(request, 'business_relatorio.html', {'relatorio': relatorio})
  

class PipelineList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = Pipeline
    template_name = 'pipeline.html'
    paginate_by = 5
    ordering = ['titulo']

    
    def get_queryset(self):
        get_pipeline = self.request.GET.get('titulo')
        if get_pipeline:
            pipeline = Pipeline.objects.filter(titulo__icontains=get_pipeline)
        else:
            pipeline = Pipeline.objects.all().order_by('titulo')
        
        return pipeline



