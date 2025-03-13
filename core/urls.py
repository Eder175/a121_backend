from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cursos/', views.cursos, name='cursos'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('change_currency/', views.change_currency, name='change_currency'),  # Rota para mudar moeda
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),  # Rota para pegar taxa
]
