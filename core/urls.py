# Substitua o conteúdo de core/urls.py
from django.urls import path
from . import views  # Importa as views do app core

urlpatterns = [
    path('', views.home, name='home'),  # Rota para a view "home"
    path('escritorio/', views.escritorio, name='escritorio'),  # Rota para o escritório
    path('cadastro/', views.cadastro, name='cadastro'),  # Rota para o cadastro
    path('login/', views.login, name='login'),  # Rota para o login
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
