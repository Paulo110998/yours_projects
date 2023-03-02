
from django.urls import path
from projectos.models import Projetos, Cards, User

from .views import ProjetosCreate, ProjetosUpdate, ProjetosDelete, ProjetosList


urlpatterns = [
    # Create
    path('criar_projeto', ProjetosCreate.as_view(), name="criar-projeto"),
    # Update
    path('editar_projeto/<int:pk>/', ProjetosUpdate.as_view(), name="editar-projeto"),
    # Delete
    path('deletar_projeto/<int:pk>/', ProjetosDelete.as_view(), name='deletar-projeto'),
    # List
    path('projetos', ProjetosList.as_view(queryset=Projetos.objects.all()), name='projetos'),
]

