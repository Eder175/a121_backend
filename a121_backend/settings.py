"""
Django settings for a121_backend project.
Generated by 'django-admin startproject' using Django 5.1.6.
Optimized by Grok (xAI) for performance, security, and scalability.
"""

import os
from pathlib import Path
import environ  # Para gerenciar variáveis de ambiente

# Inicializar o gerenciador de variáveis de ambiente
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, None),
    NGROK_HOST=(str, None),
    EMAIL_HOST_PASSWORD=(str, None),
)

# Ler o arquivo .env, se existir
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = env('SECRET_KEY', default='qYLDi7xImARDcLIAW7MNz2rD3Z9nvXEaN7qn2zbjkfIcjEWP7cMe6WFGgqiF3itZnr8')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
if 'NGROK_HOST' in os.environ:
    ALLOWED_HOSTS.append(os.environ['NGROK_HOST'])

# Application definition
INSTALLED_APPS = [
    # Apps do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps de terceiros
    'widget_tweaks',  # Para formulários personalizados
    'django_extensions',  # Ferramentas adicionais para desenvolvimento
    'django_htmx',  # Suporte para HTMX (interatividade sem JavaScript pesado)
    # Apps personalizadas
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'a121_backend.middleware.NgrokHostMiddleware',  # Middleware personalizado
    'a121_backend.middleware.RangeFileMiddleware',  # Suporte para Range
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',  # Middleware para HTMX
]

ROOT_URLCONF = 'a121_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'a121_backend.wsgi.application'

# Database - Configurado para PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='a121_backend'),
        'USER': env('DB_USER', default='postgres'),
        'PASSWORD': env('DB_PASSWORD', default='minhasenha123'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'  # Ajustado para o fuso horário do Brasil
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('pt-br', 'Português'),
    ('en', 'English'),
    ('es', 'Español'),
    ('fr', 'Français'),
    ('de', 'Deutsch'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (Uploads, Models 3D, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações de autenticação
LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'core:index'

# Configurações de sessão
SESSION_COOKIE_SECURE = False  # Defina como True em produção com HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600  # 2 semanas em segundos

# Configuração de e-mail para notificações
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='gerandoriqueza07@gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='gtpd icql xpuh fniq')
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER', default='gerandoriqueza07@gmail.com')

# Configurações de segurança para produção
SECURE_SSL_REDIRECT = False  # Defina como True em produção
SECURE_HSTS_SECONDS = 0  # Defina como 31536000 (1 ano) em produção
SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Defina como True em produção
SECURE_HSTS_PRELOAD = False  # Defina como True em produção
CSRF_COOKIE_SECURE = False  # Defina como True em produção
CSRF_COOKIE_HTTPONLY = True

# Configuração de cache (usando LocMemCache, já que Redis não está instalado)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Configuração de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'core': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}