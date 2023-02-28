from django.urls import path
from .views import Homepaginas, Sobre, Welcome
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', Homepaginas.as_view(), name="homepaginas"),
    path('sobre', Sobre.as_view(), name="sobre"),
    path('welcome', Welcome.as_view(), name='welcome'),

]