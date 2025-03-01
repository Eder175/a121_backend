from django.urls import path
from . import views  # Importa as views do app core

urlpatterns = [
    path('', views.home, name='home'),  # Rota para a view "home"
]


