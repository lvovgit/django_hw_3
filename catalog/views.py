from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def info(request):
    return render(request, 'catalog/info.html')