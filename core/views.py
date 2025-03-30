# core/views.py
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext as _
from core.models import A121CoinSupply, A121Coin, A121CoinTransaction

# Criar e treinar um modelo simples de IA emocional com TensorFlow
def create_emotion_model():
    model = Sequential([
        Dense(16, input_dim=2, activation='relu'),
        Dense(8, activation='relu'),
        Dense(4, activation='softmax')  # 4 emoções: feliz, curioso, motivado, desafiado
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    # Dados simulados para treinamento (interações e tempo de uso)
    X = np.array([[1, 2], [2, 1], [3, 5], [0, 1], [4, 3], [2, 4]])  # Exemplo: [interações, tempo]
    y = np.array([0, 1, 2, 3, 0, 2])  # 0: feliz, 1: curioso, 2: motivado, 3: desafiado
    model.fit(X, y, epochs=50, verbose=0)
    return model

# Carregar o modelo (simulado, em produção você salvaria e carregaria o modelo treinado)
emotion_model = create_emotion_model()

# Página inicial
def index(request):
    context = {
        'welcome_message': _("Bem-vindo à Revolução A121! O futuro começa aqui."),
        'quantum_transition': True,  # Ativa transição quântica na página inicial
    }
    return render(request, 'core/index.html', context)

# Página de cursos
def cursos(request):
    context = {
        'courses': [
            {'title': 'Introdução à IA para Criadores', 'description': 'Aprenda como usar IA para criar conteúdo inovador.', 'price': 249.90, 'duration': '12 horas'},
            {'title': 'Finanças para Criadores de Conteúdo', 'description': 'Domine suas finanças e lucre mais.', 'price': 199.90, 'duration': '10 horas'},
            {'title': 'Leilões Lucrativos', 'description': 'Descubra como ganhar dinheiro com leilões.', 'price': 299.90, 'duration': '15 horas'},
        ],
        'ai_recommendation': get_ai_course_recommendation(request.user) if request.user.is_authenticated else None,
    }
    return render(request, 'core/cursos.html', context)

# Cadastro de novos usuários
def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validação avançada
        if len(password) < 8:
            messages.error(request, _('A senha deve ter pelo menos 8 caracteres.'))
            return render(request, 'core/cadastro.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, _('Nome de usuário já está em uso.'))
            return render(request, 'core/cadastro.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, _('Email já está em uso.'))
            return render(request, 'core/cadastro.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, _('Usuário cadastrado com sucesso! Faça login.'))
            return redirect('core:login')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
            return render(request, 'core/cadastro.html')
    return render(request, 'core/cadastro.html')

# Login de usuários
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)
            messages.success(request, _('Login realizado com sucesso!'))
            return redirect('core:dashboard')
        else:
            messages.error(request, _('E-mail ou senha inválidos.'))
            return render(request, 'core/login.html')
    return render(request, 'core/login.html')

# Registro de novos usuários (signup)
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, _('Nome de usuário já está em uso.'))
            return render(request, 'core/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, _('Email já está em uso.'))
            return render(request, 'core/signup.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, _('Usuário registrado com sucesso! Faça login.'))
            return redirect('core:login')
        except Exception as e:
            messages.error(request, f'Erro ao registrar: {str(e)}')
            return render(request, 'core/signup.html')
    return render(request, 'core/signup.html')

# Dashboard (acessível apenas para usuários logados)
@login_required
def dashboard(request):
    # Calcular leaderboard
    leaderboard = A121Coin.objects.all().order_by('-balance')[:5]  # Top 5 usuários
    context = {
        'user': request.user,
        'a121coin_balance': A121Coin.objects.filter(user=request.user).first().balance if A121Coin.objects.filter(user=request.user).exists() else 0,
        'emotional_state': get_emotional_state(request.user),  # IA emocional
        'leaderboard': leaderboard,  # Adicionando o leaderboard ao contexto
    }
    return render(request, 'core/dashboard.html', context)

# Escritório (acessível apenas para usuários planetas)
@login_required
def escritorio(request):
    context = {
        'transactions': A121CoinTransaction.objects.filter(user=request.user).order_by('-date')[:10],
        'holographic_rewards': True,  # Ativa recompensas holográficas
    }
    return render(request, 'core/escritorio.html', context)

# Página de ganhar pontos (acessível apenas para usuários logados)
@login_required
def ganhar_pontos(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'complete_lesson':
            coin, created = A121Coin.objects.get_or_create(user=request.user, defaults={'balance': 0})
            coin.balance += 5
            coin.save()
            A121CoinTransaction.objects.create(user=request.user, amount=5, description='Lição concluída')
            messages.success(request, _('Você ganhou 5 A121Coin por completar uma lição!'))
            return redirect('core:ganhar_pontos')
    return render(request, 'core/ganhar_pontos.html')

# Detalhes do produto
def product_detail(request, product_id):
    products = {
        'iphone15': {'title': 'iPhone 15 Pro Max', 'price': 1399.00, 'description': 'Tecnologia revolucionária.'},
        'iphone16': {'title': 'iPhone 16 Pro Max', 'price': 1499.00, 'description': 'O futuro nas suas mãos.'},
    }
    context = {
        'product': products.get(product_id, {'title': 'Produto não encontrado', 'price': 0, 'description': ''}),
        'ar_enabled': True,  # Ativa visualização em AR
    }
    return render(request, 'core/product_detail.html', context)

# Mudança de moeda
def change_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        request.session['currency'] = currency
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método inválido'}, status=400)

# Obter taxas de câmbio
def get_exchange_rate(request):
    base = request.GET.get('base', 'EUR')
    rates = {
        'EUR': {'EUR': 1.0, 'USD': 1.1, 'BRL': 5.5},
        'USD': {'EUR': 0.91, 'USD': 1.0, 'BRL': 5.0},
        'BRL': {'EUR': 0.18, 'USD': 0.2, 'BRL': 1.0},
    }
    return JsonResponse({'rates': rates.get(base, rates['EUR'])})

# Interação com o chat (API para o chatbot)
@csrf_exempt
@login_required
def chat_interaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower().strip()

            if not user_message:
                return JsonResponse({'error': 'Mensagem não fornecida'}, status=400)

            response_message = simulate_grok_response(user_message, request.user)
            amount = 5 if 'lesson_completed' in user_message else 1

            transaction = A121CoinTransaction.objects.create(
                user=request.user,
                amount=amount,
                description=f'Interação com o chat: {user_message[:50]}'
            )
            total_balance = sum(t.amount for t in A121CoinTransaction.objects.filter(user=request.user))

            return JsonResponse({
                'response': response_message,
                'a121coin_balance': total_balance,
                'emotional_state': get_emotional_state(request.user),  # IA emocional
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Simulação de respostas do Grok
def simulate_grok_response(message, user):
    if 'curso' in message:
        return _('Olá! Temos cursos incríveis como "Introdução à IA para Criadores". Qual você gostaria de explorar?')
    elif 'inglês' in message or 'idioma' in message:
        return _('Vamos aprender inglês! Diga: "Hello! How are you?"')
    elif 'iphone' in message or 'produto' in message:
        return _('Temos o iPhone 15 Pro Max e o iPhone 16 Pro Max Titânio Deserto. Qual você gostaria de visualizar em AR?')
    elif 'mmn' in message or 'negócio' in message:
        return _('Nosso MMN oferece comissões de até 50% por indicação direta. Quer se juntar agora?')
    elif 'lesson_completed' in message:
        return _('Parabéns! Você ganhou 5 A121Coin por completar a lição.')
    else:
        return _('Olá! Sou o Grok, criado pela xAI. Como posso te ajudar hoje?')

# Tradução de vídeo
@csrf_exempt
def translate_video(request):
    if request.method == 'POST':
        try:
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
    messages.success(request, _('Você foi desconectado com sucesso.'))
    return redirect('core:index')

# Página de erro 404 personalizada
def error_404(request, exception=None):
    context = {
        'error_message': _('Oops! Parece que você entrou em uma dimensão paralela.'),
        'error_code': '404',
        'vr_scene': True,
    }
    response = render(request, 'core/error_404.html', context)
    response.status_code = 404
    return response

# Página de erro 500 personalizada
def error_500(request):
    context = {
        'error_message': _('Erro no núcleo quântico do sistema. Nossos engenheiros estão trabalhando para restaurar o equilíbrio.'),
        'error_code': '500',
        'vr_scene': True,
    }
    response = render(request, 'core/error_500.html', context)
    response.status_code = 500
    return response

# Função para IA emocional com TensorFlow
def get_emotional_state(user):
    # Simular dados de entrada com base no usuário
    interactions = A121CoinTransaction.objects.filter(user=user).count()
    session_time = 5  # Simulação: tempo de sessão em minutos (em produção, você coletaria isso)
    
    # Preparar entrada para o modelo
    input_data = np.array([[interactions, session_time]])
    prediction = emotion_model.predict(input_data)
    
    # Mapear a previsão para emoções
    emotions = ['feliz', 'curioso', 'motivado', 'desafiado']
    predicted_emotion = emotions[np.argmax(prediction)]
    return predicted_emotion

# Recomendações de cursos com IA
def get_ai_course_recommendation(user):
    courses = [
        'Introdução à IA para Criadores',
        'Finanças para Criadores de Conteúdo',
        'Leilões Lucrativos',
    ]
    return random.choice(courses)  # Simulação simples com random