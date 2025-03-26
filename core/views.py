# core/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'core/index.html')

def cursos(request):
    return render(request, 'core/cursos.html')

def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        # Lógica de cadastro aqui (a ser implementada)
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('core:login')
    return render(request, 'core/cadastro.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('senha')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'core/login.html')

def logout(request):
    logout(request)
    return redirect('core:index')

def dashboard(request):
    return render(request, 'core/dashboard.html')

def escritorio(request):
    return render(request, 'core/escritorio.html')

def ganhar_pontos(request):
    return render(request, 'core/ganhar_pontos.html')

def signup(request):
    # Lógica de signup (a ser implementada)
    return render(request, 'core/signup.html')

def product_detail(request, product_id):
    # Lógica para detalhes do produto (a ser implementada)
    return render(request, 'core/product_detail.html', {'product_id': product_id})

def change_currency(request):
    # Lógica para mudança de moeda (a ser implementada)
    return JsonResponse({'status': 'success'})

def get_exchange_rate(request):
    # Lógica para taxa de câmbio (a ser implementada)
    base = request.GET.get('base', 'USD')
    return JsonResponse({'rate': 1.0, 'currency': base})

@csrf_exempt
def chat_interaction(request):
    if request.method == 'POST':
        # Lógica do chat (a ser implementada)
        return JsonResponse({'response': 'Resposta do chat', 'a121coin_balance': 0})
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def translate_video(request):
    if request.method == 'POST':
        # Lógica para traduzir o vídeo (simulada por agora)
        return JsonResponse({
            'translated_audio_url': 'https://example.com/translated-audio.mp4',
            'translated_text': 'Texto traduzido (simulação).'
        })
    return JsonResponse({'error': 'Método não permitido'}, status=405)