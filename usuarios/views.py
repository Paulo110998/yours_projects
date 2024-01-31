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

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4



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

def export_users(request):
    users = User.objects.all().order_by('username') # Buscando dados dos objetos no banco e filtrando por "Título"
    
    # Criando o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Users.pdf"'

    # Criando o documento, usando o tamanho 'A4
    pdf = canvas.Canvas(response, pagesize=A4)

    # Título do Doc
    title = "RELATÓRIO DE USUÁRIOS"

    username = "Usuário: "
    email = "E-mail:"
    cadastro = "Entrou:"
    log = "Último login:"
    
    

    # Buscando os campos que eu quero adicionar ao pdf
    for user in users:
        campo1 = user.username
        campo2 = user.email
        campo3 = user.date_joined.strftime("%d/%m/%Y %H:%M:%S") if user.date_joined else "N/A"
        campo4 = user.last_login.strftime("%d/%m/%Y %H:%M:%S") if user.last_login else "N/A"
  
    
        # Adicionando informações ao PDF
        pdf.drawString(240, 800, title)

        # Subtítulos
        pdf.drawString(100, 750, username)
        pdf.drawString(100, 700, email)
        pdf.drawString(100, 650, cadastro)
        pdf.drawString(100, 500, log)

        # Dados
        pdf.drawString(150, 750, campo1)
        pdf.drawString(140, 700, campo2)
        pdf.drawString(140, 650, campo3)    
        pdf.drawString(170, 500, campo4)

        # Concluir pdf
        pdf.showPage()

    # Salvar
    pdf.save()
    return response

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
    
    

