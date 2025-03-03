from django.shortcuts import render

def home(request):
    return render(request, 'core/index.html')

def escritorio(request):
    return render(request, 'core/escritorio.html')

def cadastro(request):
    return render(request, 'core/signup.html')

def login(request):
    return render(request, 'core/login.html')
