from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta do Django (não compartilhe isso em produção!)
SECRET_KEY = 'django-insecure-_g*pi%(t$iihf!2*w(qekq=wf+n*i@djw^+@^vu97@bi4w@4q>'

# Modo de depuração (DEBUG). Em produção, defina como False.
DEBUG = False  # Alterado para False para produção

# Hosts permitidos. Em produção, especifique os domínios corretos.
ALLOWED_HOSTS = ['*']  # Temporariamente permitindo todos os hosts para testes

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',  # App core
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [BASE_DIR / 'templates'],  # Adiciona a pasta templates
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
LANGUAGE_CODE = 'pt-br'  # Alterado para português
TIME_ZONE = 'America/Sao_Paulo'  # Alterado para o fuso horário do Brasil
USE_I18N = True
USE_TZ = True

# Configuração de arquivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Adiciona a pasta static

# Configuração de campo automático padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
