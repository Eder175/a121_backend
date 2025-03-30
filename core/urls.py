# core/urls.py
from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    # Páginas principais
    path('', views.index, name='index'),
    path('cursos/', views.cursos, name='cursos'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('escritorio/', views.escritorio, name='escritorio'),
    path('ganhar-pontos/', views.ganhar_pontos, name='ganhar_pontos'),
    path('signup/', views.signup, name='signup'),
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),

    # Funcionalidades do sistema
    path('change_currency/', views.change_currency, name='change_currency'),
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),
    path('chat/', views.chat_interaction, name='chat_interaction'),
    path('translation/translate_video/', views.translate_video, name='translate_video'),

    # Páginas de erro
    path('error/404/', views.error_404, name='error_404'),
    path('error/500/', views.error_500, name='error_500'),
]