from django.shortcuts import render, redirect
from django.http import JsonResponse
from core.models import A121CoinSupply, A121Coin
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
import json

def index(request):
    return render(request, 'core/index.html')

def cursos(request):
    return render(request, 'core/cursos.html')

def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        # Verificar se o usuário ou email já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já está em uso.')
            return render(request, 'core/cadastro.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já está em uso.')
            return render(request, 'core/cadastro.html')
        # Criar o usuário
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso! Faça login.')
            return redirect('core:login')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
            return render(request, 'core/cadastro.html')
    return render(request, 'core/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('senha')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Email ou senha inválidos.')
            return render(request, 'core/login.html')
    return render(request, 'core/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        # Verificar se o usuário ou email já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já está em uso.')
            return render(request, 'core/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já está em uso.')
            return render(request, 'core/signup.html')
        # Criar o usuário
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Usuário registrado com sucesso! Faça login.')
            return redirect('core:login')
        except Exception as e:
            messages.error(request, f'Erro ao registrar: {str(e)}')
            return render(request, 'core/signup.html')
    return render(request, 'core/signup.html')

def dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar o dashboard.')
        return redirect('core:login')
    return render(request, 'core/dashboard.html')

def escritorio(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar o escritório.')
        return redirect('core:login')
    return render(request, 'core/escritorio.html')

def ganhar_pontos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar esta página.')
        return redirect('core:login')
    return render(request, 'core/ganhar_pontos.html')

def product_detail(request, product_id):
    context = {
        'product_id': product_id,
    }
    return render(request, 'core/product_detail.html', context)

def change_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency', 'EUR')
        request.session['currency'] = currency
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Requisição inválida'}, status=400)

def get_exchange_rate(request):
    base = request.GET.get('base', 'EUR')
    # Taxas de câmbio simuladas (substitua por uma chamada de API real, se necessário)
    rates = {
        'EUR': {'EUR': 1.0, 'USD': 1.1, 'BRL': 5.5},
        'USD': {'EUR': 0.91, 'USD': 1.0, 'BRL': 5.0},
        'BRL': {'EUR': 0.18, 'USD': 0.2, 'BRL': 1.0},
    }
    return JsonResponse({'rates': rates.get(base, rates['EUR'])})

def chat_interaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')

            # Lógica de resposta do A121Bot
            response_message = "Olá! Bem-vindo à A121 Evolution! Como posso te ajudar hoje?"
            if 'curso' in message.lower():
                response_message = "Recomendo o curso de Introdução à IA! Quer saber mais?"
            elif 'olá' in message.lower() or 'oi' in message.lower():
                response_message = "Oi! Como posso te ajudar hoje?"
            elif 'lesson_completed' in message.lower():
                response_message = "Parabéns por completar a lição de idioma! Você ganhou 5 A121Coin!"

            # Distribuir A121Coin por interação
            supply = A121CoinSupply.objects.first()
            if supply:
                amount = 5.00 if 'lesson_completed' in message.lower() else 1.00
                supply.distribute(
                    amount=amount,
                    user=None,  # Não associar a um usuário por agora
                    description="Interação com A121Bot" if amount == 1.00 else "Lição de idioma completada"
                )

            return JsonResponse({
                'response': response_message,
                'a121coin_balance': float(sum(t.amount for t in A121Coin.objects.all()))
            })
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Erro ao processar a interação.'}, status=500)
    return JsonResponse({'error': 'Método não permitido.'}, status=405)

def logout(request):
    auth_logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('core:index')