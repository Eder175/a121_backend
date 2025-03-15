from django.urls import path
from . import views

app_name = 'core'  # Define o namespace da aplicação

urlpatterns = [
    path('', views.index, name='index'),
    path('cursos/', views.cursos, name='cursos'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('change_currency/', views.change_currency, name='change_currency'),
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),
    path('chat/', views.chat_with_dialogflow, name='chat_with_dialogflow'),
]
