from django.urls import path
from re import template
from django.contrib.auth import views as auth_views
from re import template
from django.conf.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import  UsuarioCreate, PerfilUpdate, user_list




urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name ='login.html'), name="login"),
    
    path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path('cadastro_user/', UsuarioCreate.as_view(), name="cadastro-usuario"),
    path('cadastro_concluido/', UsuarioCreate.as_view(template_name="cadastro_concluido.html"), name="cadastro-concluido" ),
    path("update/perfil", PerfilUpdate.as_view(), name="perfil-update"),
    
    path('users_list', user_list, name='user_list'),
        
   # REDEFINIÇÃO DE SENHA DE USER
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='resetnewpassword1.html'),name='resetnewpassword'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='resetnewpassword2.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='resetnewpassword3.html'),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='resetnewpassword4.html'),name="password_reset_complete"), 

]