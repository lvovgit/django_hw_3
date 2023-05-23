from django.shortcuts import render

from catalog.models import Product


def home(request):
    context = {
        'product_list': Product.objects.all()[:3],
        'title': 'Список продуктов'
    }
    return render(request, 'catalog/home.html', context)


def info(request):
    return render(request, 'catalog/info.html')
