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

import threading
from io import BytesIO
import base64

# EXTRAINDO PDF COM REPORTLAB
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import reportlab
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# EXTRAINDO PDF COM WeasyPrint
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse

from datetime import datetime


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
        context['criar_negocio'] = 'Create Business'
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
    paginate_by = 7
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
#def quantidade_negocio(request):
 #   negocios = Negocio.objects.values_list('ticket', flat=True).distinct() 
  #  contagens = {}
   # for ticket in negocios:
    #    contagens[ticket] = Negocio.objects.filter(ticket=ticket).count() # Buscando a quantidade de tickets 
    #return render(request, 'chart.html',  {'contagens': contagens})




def chart(request):
    negocios = Negocio.objects.all()
    clientes = [negocio.cliente for negocio in negocios]
    ticket_values = [float(negocio.ticket) for negocio in negocios]
    return render(request, 'chart.html', {'clientes': clientes, 'ticket_values': ticket_values})




# Extraindo PDF com "REPORTLAB"
def get_pdf(request):
    negocios = Negocio.objects.all().order_by('cliente')
    
    # Crie o objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="customer_report.pdf"'

    # Crie o documento PDF
    #pdf = canvas.Canvas(response) 
    
    # Criar o documento PDF usando o tamanho de página 'A4'
    pdf = canvas.Canvas(response, pagesize=A4)
    
    # Título no documento
    title = "RELATÓRIO DE CLIENTES"   

    nome_cliente = "Cliente:"
    descriçao_cliente = "Descrição:"
    valor_ticket = "Ticket:"
    parceiro = "Business Partner:"
    data_de_registro = "Data de Registro:"

    # Adicionar os dados ao PDF
    for objeto in negocios:
        # Extrair os campos relevantes do objeto
        campo1 = objeto.cliente
        campo2 = objeto.descriçao
        campo3 = objeto.ticket
        campo4 = objeto.commercial_manager.username
        campo5 = objeto.data_registro.strftime("%d/%m/%Y") # Convertendo data para string com 'strftime', do módulo 'datetime'.
       

    # Adicione os dados ao documento PDF - Ex: drawString(horizontal(x), vertical(y), string )
        # Título do doc
        pdf.drawString(240, 800, title)
        
        # Subtítulos
        pdf.drawString(100, 750, nome_cliente)
        pdf.drawString(100, 700, descriçao_cliente)
        pdf.drawString(100, 650, valor_ticket)
        pdf.drawString(100, 600, parceiro)
        pdf.drawString(100, 300, data_de_registro)

        # Dados
        pdf.drawString(150, 750, campo1)
        pdf.drawString(160, 700, campo2)
        pdf.drawString(140, 650, campo3)
        pdf.drawString(200, 600, campo4)
        pdf.drawString(200, 300, campo5)
       
        # Concluir o pdf
        pdf.showPage()

    # Salvamento
    pdf.save()
    return response
    

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



