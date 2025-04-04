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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from core.models import A121CoinSupply, A121Coin, A121CoinTransaction
from django.db.models import Sum

# IA Emocional Avançada
def create_emotion_model():
    model = Sequential([
        Dense(32, input_dim=3, activation='relu'),
        Dense(16, activation='relu'),
        Dense(8, activation='relu'),
        Dense(4, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    X = np.array([[1, 2, 1], [2, 1, 3], [3, 5, 2], [0, 1, 0], [4, 3, 5], [2, 4, 1]])
    y = np.array([0, 1, 2, 3, 0, 2])
    model.fit(X, y, epochs=100, verbose=0)
    return model

emotion_model = create_emotion_model()

# View para a página inicial
def index(request):
    context = {
        'welcome_message': _("Bem-vindo à Revolução A121! O futuro começa aqui."),
        'quantum_transition': True,
    }
    return render(request, 'core/index.html', context)

# View para a página de cursos
def cursos(request):
    context = {
        'courses': [
            {'title': 'Introdução à IA', 'description': 'Aprenda os fundamentos da IA com projetos práticos.', 'price': 199.90, 'duration': '10 horas'},
            {'title': 'Finanças Pessoais', 'description': 'Domine suas finanças e planeje seu futuro.', 'price': 149.90, 'duration': '8 horas'},
            {'title': 'Realidade Aumentada', 'description': 'Crie experiências imersivas com AR.', 'price': 249.90, 'duration': '12 horas'},
        ],
    }
    return render(request, 'core/cursos.html', context)

# View para cadastro de usuários
def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        if User.objects.filter(email=email).exists():
            messages.error(request, _('Email já está em uso.'))
            return render(request, 'core/cadastro.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        A121Coin.objects.create(user=user, balance=0)
        messages.success(request, _('Cadastro concluído!'))
        return redirect('core:login')
    return render(request, 'core/cadastro.html')

# View para login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('senha')
        try:
            user = authenticate(request, username=User.objects.get(email=email).username, password=password)
            if user:
                auth_login(request, user)
                return redirect('core:dashboard')
            else:
                messages.error(request, _('Credenciais inválidas.'))
        except User.DoesNotExist:
            messages.error(request, _('Usuário não encontrado.'))
    return render(request, 'core/login.html')

# View para logout
def logout_view(request):
    auth_logout(request)
    messages.success(request, _('Você saiu com sucesso.'))
    return redirect('core:index')

# View para o dashboard
@login_required
def dashboard(request):
    a121coin_balance = A121Coin.objects.get(user=request.user).balance
    leaderboard = A121Coin.objects.order_by('-balance')[:5]
    emotional_state = predict_emotional_state(request)
    context = {
        'a121coin_balance': a121coin_balance,
        'leaderboard': leaderboard,
        'emotional_state': emotional_state,
    }
    return render(request, 'core/dashboard.html', context)

# View para o chat
@login_required
def chat_view(request):
    return render(request, 'core/chat.html')

# View para ganhar pontos
@login_required
def ganhar_pontos(request):
    if request.method == 'POST':
        user_coin = A121Coin.objects.get(user=request.user)
        user_coin.balance += 10
        user_coin.save()
        messages.success(request, _('Você ganhou 10 A121Coin!'))
        return redirect('core:dashboard')
    return render(request, 'core/ganhar_pontos.html')

# View para o escritório virtual
@login_required
def escritorio(request):
    transactions = A121CoinTransaction.objects.filter(user=request.user).order_by('-timestamp')[:10]
    context = {
        'transactions': transactions,
    }
    return render(request, 'core/escritorio.html', context)

# View para autenticação neural
@login_required
def neural_login(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'redirect': 'core:dashboard'})
    return render(request, 'core/neural_login.html')

# View para experiência em VR
@login_required
def vr_experience(request):
    return render(request, 'core/vr_experience.html')

# View para experiência em AR
@login_required
def ar_experience(request):
    return render(request, 'core/ar_experience.html')

# View para leaderboard
def leaderboard(request):
    leaderboard = A121Coin.objects.order_by('-balance')[:10]
    return JsonResponse({'leaderboard': [{'user': entry.user.username, 'balance': entry.balance} for entry in leaderboard]})

# Função para prever estado emocional
def predict_emotional_state(request):
    engagement = request.session.get('engagement', 5)
    time_spent = request.session.get('time_spent', 60)
    interactions = request.session.get('interactions', 3)
    input_data = np.array([[engagement, time_spent, interactions]])
    prediction = emotion_model.predict(input_data)
    emotional_states = ['Feliz', 'Neutro', 'Frustrado', 'Empolgado']
    return emotional_states[np.argmax(prediction)]

# API para interações de chat
@csrf_exempt
def chat_interaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        user = request.user if request.user.is_authenticated else None
        response_message = "Entendido! Como posso te ajudar mais?" if message else "Por favor, envie uma mensagem válida."
        if user:
            user_coin = A121Coin.objects.get(user=user)
            if message == 'lesson_completed':
                user_coin.balance += 5
                user_coin.save()
            return JsonResponse({
                'response': response_message,
                'a121coin_balance': user_coin.balance,
            })
        return JsonResponse({'response': response_message, 'a121coin_balance': 0})
    return JsonResponse({'error': 'Método não permitido'}, status=405)

# APIView para interações de chat (RESTful)
class ChatInteractionAPIView(APIView):
    def post(self, request):
        message = request.data.get('message', '')
        user = request.user if request.user.is_authenticated else None
        response_message = "Entendido! Como posso te ajudar mais?" if message else "Por favor, envie uma mensagem válida."
        if user:
            user_coin = A121Coin.objects.get(user=user)
            if message == 'lesson_completed':
                user_coin.balance += 5
                user_coin.save()
            return Response({
                'response': response_message,
                'a121coin_balance': user_coin.balance,
            }, status=status.HTTP_200_OK)
        return Response({'response': response_message, 'a121coin_balance': 0}, status=status.HTTP_200_OK)

# ViewSet para transações A121Coin
class A121CoinTransactionViewSet(viewsets.ModelViewSet):
    queryset = A121CoinTransaction.objects.all()
    serializer_class = None  # Adicione um serializer se necessário
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)