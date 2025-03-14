from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    return render(request, 'core/index.html', {'section': 'index'})

def cursos(request):
    return render(request, 'core/index.html', {'section': 'cursos'})

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Validação simples
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'core/cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return render(request, 'core/cadastro.html')

        # Criar o usuário
        user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
        return redirect('core:login')

    return render(request, 'core/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('core:index')
        else:
            messages.error(request, 'E-mail ou senha incorretos.')
            return render(request, 'core/login.html')

    return render(request, 'core/login.html')

def get_exchange_rate(request):
    base_currency = request.GET.get('base', 'EUR')
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse({'success': True, 'rates': data['rates']})
    return JsonResponse({'success': False, 'error': 'Failed to fetch exchange rates'})

def change_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        if currency in ['EUR', 'USD', 'BRL']:
            request.session['currency'] = currency
            return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid currency'})
