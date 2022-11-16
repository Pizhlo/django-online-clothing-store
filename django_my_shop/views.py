from django.http import HttpResponse
from django.shortcuts import render
from shop.models import *
from django.core.handlers.wsgi import WSGIRequest


def home(request: WSGIRequest) -> HttpResponse:
    """Главная страница сайта"""
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'main.html', {'categories': categories,
                                         'products': products})
