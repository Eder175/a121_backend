from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='home'),  # Página inicial
    path('escritorio/', views.escritorio, name='escritorio'),  # Página do escritório
    path('cadastro/', views.cadastro_view, name='cadastro'),  # Página de cadastro
    path('login/', views.login_view, name='login'),  # Página de login
    path('produto/<int:product_id>/', views.product_detail, name='product_detail'),  # Detalhes do produto
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard de vendedores
    path('ganhar-pontos/', views.ganhar_pontos, name='ganhar_pontos'),  # Ganhar pontos (gamificação)
    path('cursos/', views.cursos, name='cursos'),  # Página de cursos
]
