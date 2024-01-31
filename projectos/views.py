# Views de Crud e Lis
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import DetailView
# Views de Autenticação
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.auth.models import User
# Configura uma página de erro mais bonita e clean
from django.shortcuts import get_object_or_404 
# Importando models dos projectos
from .models import Projetos, List
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils.encoding import smart_str
# view para checkbox no html
from django.shortcuts import render
from .forms import Checkbox


########## CREATE ##############
# PROJETOS
class ProjetosCreate(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    login_url = '/login/' # Só acessa a pagina se tiver logado
    redirect_field_name = 'login' # Redireciona para o login
    group_required = [u'Managers', u'Assistants'] # Acesso restrito por grupos
    model = Projetos # Model
    fields = ['titulo', 'descriçao', 'criador'] # Adiciono os campos de cadastros que devem aparecer
    template_name = 'projetos/criarprojetos.html' # Template
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

# PROJETOS - UPDATE
class ProjetosUpdate(UpdateView, GroupRequiredMixin, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers']
    model = Projetos
    fields = ['titulo', 'descriçao', 'criador']
    template_name = 'projetos/updateprojeto.html'
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


# PROJETOS - DELETE
class ProjetosDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url ='/login/'     
    redirect_field_name = 'login'
    group_required = [u'Managers']
    models = Projetos
    template_name = 'projetos/excluirprojeto.html'
    success_url = reverse_lazy('welcome')  

    
    def get_context_data(self, *args , **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['excluir_projeto'] = 'Excluír Projeto'
        return context
    
    def form_valid(self, form):
        url = super().form_valid(form)
        messages.success(self.request,"Projeto Excluído!")
        return url
    

# PROJETOS - LIST
class ProjetosList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    models = Projetos
    template_name = 'welcome.html'
    paginate_by = 8
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



class ProjetosDetail(DetailView):
    model = Projetos
    template_name ="projetos/projeto_detail.html"
    context_object_name = "projetos_detail"




def export_projetos(request):
    projetos = Projetos.objects.all().order_by('titulo') # Buscando dados dos objetos no banco e filtrando por "Título"

    # Criando o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Your_Projects.pdf"'

    # Criando o documento, usando o tamanho 'A4
    pdf = canvas.Canvas(response, pagesize=A4)

    # Título do Doc
    title = "YOUR PROJECTS"

    titulo_projeto = "Projeto:"
    descriçoes = "Descrição:"
    manager = "Manager:"
    data = "Data de Registro:"
    

    # Buscando os campos que eu quero adicionar ao pdf
    for projeto in projetos:
        campo1 = projeto.titulo
        campo2 = projeto.descriçao
        campo3 = projeto.criador.username
        campo4 = projeto.data_registro.strftime("%d/%m/%Y")
    
        # Adicionando informações ao PDF
        pdf.drawString(240, 800, title)

        # Subtítulos
        pdf.drawString(100, 750, titulo_projeto)
        pdf.drawString(100, 700, descriçoes)
        pdf.drawString(100, 650, manager)
        pdf.drawString(100, 300, data)

        # Dados
        pdf.drawString(150, 750, campo1)
        pdf.drawString(160, 700, campo2)
        pdf.drawString(150, 650, campo3)    
        pdf.drawString(200, 300, campo4)

        # Concluir pdf
        pdf.showPage()

    # Salvar
    pdf.save()
    return response


################## LISTAS - CREATE ##############################
class ListCreate(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = List
    fields = ['titulo', 'prioridade', 'projetos', 'criador']
    template_name= "listas/criar_lista.html"
    success_url = reverse_lazy('listar-list') 
    
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, "Lista criada com sucesso!") # Mensagem que deve aparecer no template
        return url
  
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['criar_lista'] = 'Criar Lista'
        return context
    
    
# LISTAS - UPDATE
class ListUpdate(UpdateView, GroupRequiredMixin, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = List
    fields = ['titulo', 'prioridade', 'projetos']
    template_name = 'listas/update_lista.html'
    success_url = reverse_lazy('listar-list')

    
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['editar_lista'] = 'Editar Lista'
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, "Lista atualizada!") # Mensagem que deve aparecer no template
        return url


# LISTAS - DELETE
class ListDelete(DeleteView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = List
    template_name = "listas/list_delete.html"
    success_url = reverse_lazy('listar-list')

    def get_context_data(self, *args , **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['excluir_cards'] = 'Excluír Card'
        return context
    
    def form_valid(self, form):
        url = super().form_valid(form)
        messages.success(self.request,"Lista Excluída!")
        return url

    
# LISTAS - LIST
class ListList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    group_required = [u'Managers', u'Assistants']
    model = List
    template_name = 'listas/listas.html'
    paginate_by = 4
    ordering = ['titulo'] # Ordenando a listagem por 'titulo'

    
    # Método que por padrão lista todos os objetos criados
    def get_queryset(self):
        get_cards = self.request.GET.get('titulo')
        if get_cards:
            cards = List.objects.filter(titulo__icontains=get_cards)
        else:
            cards = List.objects.all().order_by('titulo') # Ordenando a listagem dos objetos
        
        return cards
    

def export_list(request):
    listas = List.objects.all().order_by('titulo')

    # Criando o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Your_List.pdf"'

    # Criando o documento, usando o tamanho A4
    pdf = canvas.Canvas(response, pagesize=A4)

    # Título do doc
    title = "YOUR LIST"

    name_list = 'Lista:'
    prioridades = "Prioridade:"
    projetos = "Projetos:"
    manager = "Manager: "
    data = "Data de Registro:"
    
    for lista in listas:
        campo1 = lista.titulo.encode('utf-8', 'ignore') if lista.titulo else "Campo 1 - Não condificável" # Se o campo não for utf8, escreve essa string no pdf
        campo3 = lista.prioridade.encode('utf-8', 'ignore') if lista.prioridade else "Campo 3 - Não Condificável"
        campo4 = lista.projetos.titulo.encode('utf-8', 'ignore') if lista.projetos else "Não condificável"
        campo5 = lista.criador.username.encode('utf-8', 'ignore') if lista.criador.username else "Não condificável"
        campo6 = lista.data_registro.strftime("%d/%m/%Y")
        
        # Adicionando informações ao pdf
        pdf.drawString(265, 800, title)

        # Subtítulos
        pdf.drawString(100, 750, name_list)
        pdf.drawString(100, 700, prioridades)
        pdf.drawString(100, 650, projetos)
        pdf.drawString(100, 600, manager)
        pdf.drawString(100, 300, data)

        # Dados
        pdf.drawString(130, 750, campo1)
        pdf.drawString(160, 700, campo3)
        pdf.drawString(150, 650, campo4)
        pdf.drawString(155, 600, campo5)
        pdf.drawString(195, 300, campo6)
    

        # Concluir PDF
        pdf.showPage()
    
    # Salvar
    pdf.save()
    return response





# View para checkbox no html
# def minha_visualizacao(request):
    #if request.method == 'POST':
      #  form = Checkbox(request.POST)
     #   if form.is_valid():
    #        metodo_selecionado = form.cleaned_data['metodo']
   #         # Faça algo com o método selecionado, como redirecionar para outra página ou processar os dados
  #          return render(request, 'list_update.html', {'metodo_selecionado': metodo_selecionado})
 #   else:
#        form = Checkbox()
#    return render(request, 'list_update.html', {'form': form})









    
    
    