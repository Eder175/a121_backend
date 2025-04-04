# core/urls.py
from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    # Páginas principais
    path('', views.index, name='index'),
    path('cursos/', views.cursos, name='cursos'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Adicionado para corrigir NoReverseMatch
    path('chat/', views.chat_view, name='chat'),
    
    # Funcionalidades de gamificação e pontos
    path('ganhar-pontos/', views.ganhar_pontos, name='ganhar_pontos'),
    path('escritorio/', views.escritorio, name='escritorio'),
    
    # Interações com IA e chat
    path('chat-interaction/', views.chat_interaction, name='chat_interaction'),
    
    # Autenticação neural
    path('neural-login/', views.neural_login, name='neural_login'),
    
    # APIs para VR/AR
    path('vr-experience/', views.vr_experience, name='vr_experience'),
    path('ar-experience/', views.ar_experience, name='ar_experience'),
    
    # Leaderboard e gamificação
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]