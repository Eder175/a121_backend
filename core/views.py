from django.shortcuts import render
from .models import Produto, Venda
from django.db.models import Sum

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'core/index.html', {'produtos': produtos})

def escritorio(request):
    return render(request, 'core/escritorio.html')

def cadastro(request):
    return render(request, 'core/signup.html')

def login(request):
    return render(request, 'core/login.html')

def product_detail(request, product_id):
    produto = Produto.objects.get(id=product_id)
    return render(request, 'core/product_detail.html', {'produto': produto})

def dashboard(request):
    sales_by_country = Venda.objects.values('country').annotate(total=Sum('amount'))
    global_sales = Venda.objects.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'core/dashboard.html', {'sales_by_country': sales_by_country, 'global_sales': global_sales})
