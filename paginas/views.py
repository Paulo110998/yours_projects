from django.views.generic import TemplateView



# Create your views here.
class Homepaginas(TemplateView):
    template_name = "home.html"

class Sobre(TemplateView):
    template_name = "sobre.html"


class Welcome(TemplateView):
    template_name = "welcome.html"


