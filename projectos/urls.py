
from django.urls import path
from projectos.models import Projetos, List, User

from .views import ProjetosCreate, ProjetosUpdate, ProjetosDelete, ProjetosList, ProjetosDetail
from . views import ListCreate, ListUpdate, ListDelete, ListList, export_projetos
from usuarios.models import User
from . import views 


urlpatterns = [
    # Create Projeto
    path('criar_projeto', ProjetosCreate.as_view(), name="criar-projeto"),
    # Update Projeto
    path('editar_projeto/<int:pk>/', ProjetosUpdate.as_view(queryset=Projetos.objects.all()), name="editar-projeto"),
    # Delete Projeto
    path('deletar_projeto/<int:pk>/', ProjetosDelete.as_view(queryset=Projetos.objects.all()), name='deletar-projeto'),
    # List Projeto
    path('welcome_user', ProjetosList.as_view(queryset=Projetos.objects.all()), name='welcome'),
    # Projetos Detail
    path('projeto/<int:pk>/', ProjetosDetail.as_view(), name='projeto-detalhe'),
    # Exportando Projeto
    path('export_projects', views.export_projetos, name="export_projetos"),

    # Create Cards
    path('create_list', ListCreate.as_view(), name='criar-list'),
    
    # Update Cards
    path('update_list/<int:pk>/', ListUpdate.as_view(queryset=List.objects.all()), name='editar-list'),
    # Delete Cards
    path('delete_list/<int:pk>/', ListDelete.as_view(queryset=List.objects.all()), name='deletar-list'),
    # List Card
    path('your_lists', ListList.as_view(queryset=List.objects.all()), name='listar-list'),
    path('export_list', views.export_list, name="export_list"),
    




    
    

    
]

