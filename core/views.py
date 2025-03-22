from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def index(request):
    return render(request, 'core/index.html', {'section': 'index'})

def cursos(request):
    return render(request, 'core/index.html', {'section': 'cursos'})

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('core:index')
    else:
        form = UserCreationForm()
    return render(request, 'core/index.html', {'section': 'cadastro', 'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('core:index')
    else:
        form = AuthenticationForm()
    return render(request, 'core/index.html', {'section': 'login', 'form': form})

@csrf_exempt
def change_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency', 'EUR')
        request.session['currency'] = currency
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def get_exchange_rate(request):
    # Simulação de taxas de câmbio
    rates = {
        'EUR': 1.0,
        'USD': 1.1,
        'BRL': 5.5
    }
    return JsonResponse({'success': True, 'rates': rates})

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        # Temporariamente, retorna uma mensagem padrão até implementarmos o novo chatbot
        return JsonResponse({'response': 'Olá! Estou sendo atualizado para ser o chatbot mais inteligente do mundo! Volte em breve!'})
    return JsonResponse({'error': 'Método não permitido'}, status=405)