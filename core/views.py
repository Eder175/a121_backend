from django.shortcuts import render
from django.http import JsonResponse
import requests
from .models import Produto

def index(request):
    produtos = Produto.objects.all()
    return render(request, 'core/index.html', {'produtos': produtos, 'section': 'index'})

def cursos(request):
    return render(request, 'core/index.html', {'section': 'cursos'})

def cadastro(request):
    return render(request, 'core/cadastro.html')

def login(request):
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
