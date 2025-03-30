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

# IA Emocional
def create_emotion_model():
    model = Sequential([
        Dense(16, input_dim=2, activation='relu'),
        Dense(8, activation='relu'),
        Dense(4, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    X = np.array([[1, 2], [2, 1], [3, 5], [0, 1], [4, 3], [2, 4]])
    y = np.array([0, 1, 2, 3, 0, 2])
    model.fit(X, y, epochs=50, verbose=0)
    return model

emotion_model = create_emotion_model()

def index(request):
    context = {
        'welcome_message': _("Bem-vindo à Revolução A121! O futuro começa aqui."),
        'quantum_transition': True,
    }
    return render(request, 'core/index.html', context)

def cursos(request):
    context = {
        'courses': [
            {'title': 'Introdução à IA', 'description': 'Aprenda IA.', 'price': 199.90, 'duration': '10 horas'},
            {'title': 'Finanças Pessoais', 'description': 'Domine finanças.', 'price': 149.90, 'duration': '8 horas'},
        ],
    }
    return render(request, 'core/cursos.html', context)

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
        messages.success(request, _('Cadastro concluído!'))
        return redirect('core:login')
    return render(request, 'core/cadastro.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('senha')
        user = authenticate(request, username=User.objects.get(email=email).username, password=password)
        if user:
            auth_login(request, user)
            return redirect('core:dashboard')
        messages.error(request, _('Credenciais inválidas.'))
    return render(request, 'core/login.html')

@login_required
def chat_view(request):
    return render(request, 'core/chat.html')