from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .models import Projetos, List
# Register your models here.
admin.site.register(Projetos)
admin.site.register(List)



