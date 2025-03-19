from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from google.cloud import dialogflow_v2 as dialogflow
import os

# Configuração do Dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), '../a121bot-credentials.json')
DIALOGFLOW_PROJECT_ID = 'a121bot'  # Substitua pelo ID real do seu projeto Dialogflow
DIALOGFLOW_LANGUAGE_CODE = 'pt-BR'
SESSION_ID = 'a121-session'

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
def chat_with_dialogflow(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        try:
            session_client = dialogflow.SessionsClient()
            session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
            text_input = dialogflow.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
            query_input = dialogflow.QueryInput(text=text_input)
            response = session_client.detect_intent(session=session, query_input=query_input)
            return JsonResponse({'response': response.query_result.fulfillment_text})
        except Exception as e:
            print(f"Erro no Dialogflow: {e}")  # Log do erro para depuração
            return JsonResponse({'response': 'Desculpe, houve um problema. Tente novamente ou me dê mais detalhes.'})
    return JsonResponse({'error': 'Método não permitido'}, status=405)
