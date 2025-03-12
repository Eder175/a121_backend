from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('escritorio/', views.escritorio, name='escritorio'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('produto/<int:product_id>/', views.product_detail, name='product_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
