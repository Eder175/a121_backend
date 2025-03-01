from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta (não compartilhe isso publicamente!)
SECRET_KEY = 'django-insecure-_g*pi%(t$iihf!2*w(qekq=wf+n*i@djw^+@^vu97@bi4w@4q>'

# Modo de depuração (DEBUG) - desative em produção!
DEBUG = True

# Hosts permitidos (adicione o domínio do Render quando publicar)
ALLOWED_HOSTS = ['*']  # Permite todos os hosts (apenas para desenvolvimento)

# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',  # App core
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configurações de URLs
ROOT_URLCONF = 'a121_backend.urls'

# Configurações de templates
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

# Configurações do WSGI
WSGI_APPLICATION = 'a121_backend.wsgi.application'

# Configurações do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configurações de idioma e fuso horário
LANGUAGE_CODE = 'pt-br'  # Alterado para português
TIME_ZONE = 'America/Sao_Paulo'  # Alterado para o fuso horário do Brasil
USE_I18N = True
USE_TZ = True

# Configurações de arquivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Adiciona a pasta static

# Configurações de campo automático
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
