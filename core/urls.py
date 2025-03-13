from django.urls import path
from . import views

app_name = 'core'  # Adicionado para suportar o namespace no a121_backend/urls.py

urlpatterns = [
    path('', views.index, name='index'),
    path('cursos/', views.cursos, name='cursos'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('change_currency/', views.change_currency, name='change_currency'),
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),
]
