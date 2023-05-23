import os

from django.shortcuts import render

from catalog.models import Product
from config import settings


def home(request):
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path + '/images')
    context = {
        'product_list': Product.objects.all()[:4],
        'title': 'Список продуктов',
        'images': img_list
    }
    return render(request, 'catalog/home.html', context)


def info(request):
    return render(request, 'catalog/info.html')
