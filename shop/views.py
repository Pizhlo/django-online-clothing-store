from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from django.core.handlers.wsgi import WSGIRequest
from typing import Union


def home(request: WSGIRequest) -> HttpResponse:
    """Главная страница магазина"""
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})


def product_detail(request: WSGIRequest, product_id: int, product_slug: str) -> HttpResponse:
    """Функция отображения конкретного товара"""
    product = get_object_or_404(Product,
                                id=product_id,
                                slug=product_slug,
                                available=True)
    # cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product})


def product_list_by_category(request: WSGIRequest, slug: str) -> HttpResponse:
    """Функция отображения всех доступных товаров"""
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    products = Product.objects.filter(category=category, available=True)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

