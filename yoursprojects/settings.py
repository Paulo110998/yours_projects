"""
Django settings for yoursprojects project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from telnetlib import LOGOUT
import os
import django_on_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^!apz-vgmb8b64t=7f=c2u3omo9o6(kbhcd%nb#53ene(wchm0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #Serve para as mensagens de erros apareçam em fase de desenvolvimento, ao fazer deploy, temos que retirar.

ALLOWED_HOSTS = ['*'] # Ao fazer deploy, temos que especificar o domínio da aplicação dentro do ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paginas.apps.PaginasConfig',
    'usuarios.apps.UsuariosConfig',
    'crispy_forms',
    'django_cleanup.apps.CleanupConfig',
    'projectos.apps.ProjectosConfig',
    'business.apps.BusinessConfig',
    
]

# MIDDLEWARE = Mediador entre o cliente e o servidor - EX: Browser(cliente) -> Middleware <- Servidor
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoise.Middleware', # White Noise -> Serve para arquivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yoursprojects.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #definindo nome padrão para templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI = Padrão de aplicação web python, o django segue esse padrão.
WSGI_APPLICATION = 'yoursprojects.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yoursprojects',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1', 
        'PORT': '3306', 

    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/' # Usando durando o desenvolvimento

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Usando em produção

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# ARQUIVOS DE MEDIA/UPLOAD

#Direcionando os uploads para uma pasta do projeto chamada "uploads"
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_URL = '/uploads/' # Constante que possibilita a vizualização do arquivo

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CONFIGURAÇÃO DE AUTENTICAÇÃO (Login/Logout) -> Controle de entrada e saída do usuário

LOGIN_REDIRECT_URL = 'welcome' # Após o login, redireciona para o 'welcome'

LOGIN_URL = "login" # Redireciona para a url de login

LOGOUT_REDIRECT = "login"


# REDEFINIÇÃO DE SENHA (Configurações para envio de e-mail)

# S M T P -> Simple Mail Transfer Protocol (Protocolo de envio de e-mail simples).
#Mime -> É uma norma de envio de mensagens pela internet, padrão de envio de mensagem códificado.

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

# Conexão com o servidor do gmail
DEFAULT_FROM_EMAIL = 'Yours Projects'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = "587"
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'testes.djangoframe@gmail.com'
EMAIL_HOST_PASSWORD = "yhxkbvfujatnenaz"

server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)

django_on_heroku.settings(locals())