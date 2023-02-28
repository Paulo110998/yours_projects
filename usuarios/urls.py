from django.urls import path
from re import template
from django.contrib.auth import views as auth_views
from re import template
from django.conf.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import Welcome, UsuarioCreate, PerfilUpdate


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name ='login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path('welcome/', Welcome.as_view(template_name="welcome.html"), name="welcome"),
    path('cadastro_user/', UsuarioCreate.as_view(), name="cadastro-usuario"),
    path('cadastro_concluido/', UsuarioCreate.as_view(template_name="cadastro_concluido.html"), name="cadastro-concluido" ),
    path("update_perfil/user",PerfilUpdate.as_view(), name="perfil_update" ),

    

    
]