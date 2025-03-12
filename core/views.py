from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

def escritorio(request):
    return render(request, 'core/escritorio.html')

def cadastro_view(request):
    return render(request, 'core/cadastro.html')

def login_view(request):
    return render(request, 'core/login.html')

def product_detail(request, product_id):
    return render(request, 'core/product_detail.html', {'product_id': product_id})

def dashboard(request):
    return render(request, 'core/dashboard.html')

def ganhar_pontos(request):
    return render(request, 'core/ganhar_pontos.html')

def cursos(request):
    return render(request, 'core/cursos.html')
