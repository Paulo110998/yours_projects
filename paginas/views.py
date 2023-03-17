from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class Homepaginas(TemplateView):
    template_name = "home.html"

class Sobre(TemplateView):
    template_name = "sobre.html"


class Welcome(TemplateView):
    template_name = "welcome.html"