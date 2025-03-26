# core/urls.py
from django.urls import path, include
from core import views

app_name = 'core'

urlpatterns = [
    # Páginas principais
    path('', views.index, name='index'),  # Mapeia para index.html
    path('cursos/', views.cursos, name='cursos'),  # Mapeia para cursos.html
    path('cadastro/', views.cadastro, name='cadastro'),  # Mapeia para cadastro.html
    path('login/', views.login, name='login'),  # Mapeia para login.html
    path('logout/', views.logout, name='logout'),  # Mapeia para a view logout
    path('dashboard/', views.dashboard, name='dashboard'),  # Mapeia para dashboard.html
    path('escritorio/', views.escritorio, name='escritorio'),  # Mapeia para escritorio.html
    path('ganhar-pontos/', views.ganhar_pontos, name='ganhar_pontos'),  # Mapeia para ganhar_pontos.html
    path('signup/', views.signup, name='signup'),  # Mapeia para signup.html
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  # Mapeia para product_detail.html

    # Funcionalidades
    path('change_currency/', views.change_currency, name='change_currency'),
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),
    path('chat/', views.chat_interaction, name='chat_interaction'),

    # Namespace para tradução
    path('translation/', include([
        path('translate_video/', views.translate_video, name='translate_video'),
    ], namespace='translation')),
]