from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta do Django (não compartilhe isso em produção!)
SECRET_KEY = 'django-insecure-_g*pi%(t$iihf!2*w(qekq=wf+n*i@djw^+@^vu97@bi4w@4q>'

# Modo de depuração (DEBUG). Em produção, defina como False.
DEBUG = True  # Temporariamente True para testes locais; mude para False antes de deploy no Render

# Hosts permitidos. Em produção, especifique os domínios corretos.
ALLOWED_HOSTS = ['a121-backend.onrender.com', 'localhost', '127.0.0.1']

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',  # Para servir estáticos
    'core.apps.CoreConfig',  # App core
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para arquivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuração das URLs
ROOT_URLCONF = 'a121_backend.urls'

# Configuração dos templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Configuração do WSGI
WSGI_APPLICATION = 'a121_backend.wsgi.application'

# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuração de idioma e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Pao Paulo'
USE_I18N = True
USE_TZ = True

# Configuração de arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Para produção com Whitenoise

# Configuração de cookies e segurança
SESSION_COOKIE_AGE = 1209600  # 2 semanas em segundos
SESSION_COOKIE_SECURE = not DEBUG  # True em produção com HTTPS
CSRF_COOKIE_SECURE = not DEBUG  # True em produção com HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = not DEBUG  # Redireciona para HTTPS em produção

# Configuração de campo automático padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
