from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('cursos/', views.cursos, name='cursos'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('change_currency/', views.change_currency, name='change_currency'),
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),
    path('chat/', views.chat, name='chat'),  # Alterado de 'chat_with_dialogflow' para 'chat'
]