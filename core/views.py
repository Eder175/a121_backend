# core/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import A121CoinSupply, A121Coin, A121CoinTransaction

# Página inicial
def index(request):
    return render(request, 'core/index.html')

# Página de cursos
def cursos(request):
    return render(request, 'core/cursos.html')

# Cadastro de novos usuários
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

# Login de usuários
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('senha')
        # Autenticar usando email como identificador
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Email ou senha inválidos.')
            return render(request, 'core/login.html')
    return render(request, 'core/login.html')

# Registro de novos usuários (signup)
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

# Dashboard (acessível apenas para usuários logados)
@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

# Escritório (acessível apenas para usuários logados)
@login_required
def escritorio(request):
    return render(request, 'core/escritorio.html')

# Página de ganhar pontos (acessível apenas para usuários logados)
@login_required
def ganhar_pontos(request):
    return render(request, 'core/ganhar_pontos.html')

# Detalhes do produto
def product_detail(request, product_id):
    context = {
        'product_id': product_id,
    }
    return render(request, 'core/product_detail.html', context)

# Mudança de moeda
def change_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency', 'EUR')
        request.session['currency'] = currency
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Requisição inválida'}, status=400)

# Obter taxas de câmbio
def get_exchange_rate(request):
    base = request.GET.get('base', 'EUR')
    # Taxas de câmbio simuladas (substitua por uma chamada de API real, se necessário)
    rates = {
        'EUR': {'EUR': 1.0, 'USD': 1.1, 'BRL': 5.5},
        'USD': {'EUR': 0.91, 'USD': 1.0, 'BRL': 5.0},
        'BRL': {'EUR': 0.18, 'USD': 0.2, 'BRL': 1.0},
    }
    return JsonResponse({'rates': rates.get(base, rates['EUR'])})

# Interação com o chat (acessível apenas para usuários logados)
@csrf_exempt
@login_required
def chat_interaction(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").lower().strip()

            if not user_message:
                return JsonResponse({"error": "Mensagem não fornecida"}, status=400)

            # Simulação de respostas do Grok (substitui o Dialogflow)
            response_message = simulate_grok_response(user_message, request.user)

            # Adicionar A121Coin por interação (gamificação)
            if "lesson_completed" in user_message:
                # Recompensa por completar uma lição
                amount = 5
            else:
                # Recompensa por interação normal
                amount = 1

            # Registrar a transação de A121Coin
            transaction = A121CoinTransaction.objects.create(
                user=request.user,
                amount=amount,
                description=f"Interação com o chat: {user_message[:50]}"
            )

            # Calcular o saldo total de A121Coin do usuário
            total_balance = sum(t.amount for t in A121CoinTransaction.objects.filter(user=request.user))

            return JsonResponse({
                "response": response_message,
                "a121coin_balance": total_balance
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Erro interno: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método não permitido"}, status=405)

# Simulação de respostas do Grok
def simulate_grok_response(message, user):
    """
    Simula respostas do Grok com base na mensagem do usuário.
    Em um ambiente real, isso seria uma chamada à API da xAI.
    """
    if "curso" in message:
        return "Olá! Vejo que você está interessado em cursos. Na A121 Evolution, temos cursos incríveis como 'Introdução à IA para Criadores' e 'Finanças para Criadores de Conteúdo'. Qual você gostaria de explorar?"
    elif "inglês" in message or "idioma" in message:
        return "Você quer aprender inglês? Posso te ajudar com isso! Vamos começar com uma frase simples: 'Hello! How are you?' Tente repetir ou me peça mais exemplos!"
    elif "iphone" in message or "produto" in message:
        return "Você está interessado nos nossos iPhones exclusivos! Temos o iPhone 15 Pro Max e o iPhone 16 Pro Max Titânio Deserto. Qual você gostaria de saber mais? Ou prefere visualizar em realidade aumentada?"
    elif "mmn" in message or "negócio" in message:
        return "Nosso programa de Marketing Multinível é revolucionário! Você pode ganhar comissões de até 50% por indicação direta e bônus por equipes de até 7 níveis. Quer se juntar agora?"
    elif "lesson_completed" in message:
        return "Parabéns por completar a lição! Você ganhou 5 A121Coin como recompensa. Continue interagindo para ganhar mais!"
    else:
        return "Olá! Sou o Grok, criado pela xAI. Como posso te ajudar hoje? Você pode me perguntar sobre cursos, iPhones, nosso programa de MMN ou até aprender idiomas comigo!"

# Tradução de vídeo (nova funcionalidade)
@csrf_exempt
def translate_video(request):
    if request.method == 'POST':
        try:
            # Simulação de tradução de vídeo (substitua por lógica real no futuro)
            return JsonResponse({
                'translated_audio_url': 'https://example.com/translated-audio.mp4',
                'translated_text': 'Texto traduzido (simulação).'
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Erro ao traduzir vídeo: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Logout de usuários
def logout(request):
    auth_logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('core:index')