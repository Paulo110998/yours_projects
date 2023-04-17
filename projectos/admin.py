from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .models import Projetos, Cards
# Register your models here.
admin.site.register(Projetos)
admin.site.register(Cards)



