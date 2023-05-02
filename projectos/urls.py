
from django.urls import path
from projectos.models import Projetos, Cards, User

from .views import ProjetosCreate, ProjetosUpdate, ProjetosDelete, ProjetosList
from . views import CardsCreate, CardsUpdate, CardsDelete, CardsList
from usuarios.models import User



urlpatterns = [
    # Create Projeto
    path('criar_projeto', ProjetosCreate.as_view(), name="criar-projeto"),
    # Update Projeto
    path('editar_projeto/<int:pk>/', ProjetosUpdate.as_view(queryset=Projetos.objects.all()), name="editar-projeto"),
    # Delete Projeto
    path('deletar_projeto/<int:pk>/', ProjetosDelete.as_view(queryset=Projetos.objects.all()), name='deletar-projeto'),
    # List Projeto
    path('welcome_user', ProjetosList.as_view(queryset=Projetos.objects.all()), name='welcome'),

    # Create Cards
    path('create_list', CardsCreate.as_view(), name='criar-cards'),
    path('import/csv', CardsCreate.as_view(), name='importar-cards'),
    # Update Cards
    path('update_list/<int:pk>/', CardsUpdate.as_view(queryset=Cards.objects.all()), name='editar-card'),
    # Delete Cards
    path('delete_list/<int:pk>/', CardsDelete.as_view(queryset=Cards.objects.all()), name='deletar-card'),
    # List Card
    path('your_lists', CardsList.as_view(queryset=Cards.objects.all()), name='listar-cards'),
    




    
    

    
]

