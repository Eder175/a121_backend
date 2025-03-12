"""
URL configuration for a121_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Define as rotas principais do projeto
urlpatterns = [
    path('admin/', admin.site.urls),  # URL para o painel de administração do Django
    path('', include('core.urls')),  # Inclui as URLs do app core (definidas em core/urls.py)
    path('login/', include('core.urls')),  # Inclui as URLs para login
    path('cadastro/', include('core.urls')),  # Inclui as URLs para cadastro
    path('cursos/', include('core.urls')),  # Inclui as URLs para cursos
    path('dashboard/', include('core.urls')),  # Inclui as URLs para dashboard
    path('escritorio/', include('core.urls')),  # Inclui as URLs para escritório
    path('produto/<int:product_id>/', include('core.urls')),  # Inclui as URLs para detalhes de produto
    path('ganhar-pontos/', include('core.urls')),  # Inclui as URLs para ganhar pontos
]

# Serve arquivos estáticos e de mídia durante o desenvolvimento (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
