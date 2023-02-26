from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class Homepaginas(TemplateView):
    template_name = "home.html"

class Sobre(TemplateView):
    template_name = "sobre.html"