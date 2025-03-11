# Substitua o conteúdo de views.py
from django.shortcuts import render
from .models import Product, Sale

def home(request):
    return render(request, 'core/index.html')

def escritorio(request):
    return render(request, 'core/escritorio.html')

def cadastro(request):
    return render(request, 'core/signup.html')

def login(request):
    return render(request, 'core/login.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def dashboard(request):
    sales_by_country = Sale.objects.values('country').annotate(total=models.Sum('amount'))
    global_sales = Sale.objects.aggregate(total=models.Sum('amount'))['total'] or 0
    return render(request, 'dashboard.html', {'sales_by_country': sales_by_country, 'global_sales': global_sales})
