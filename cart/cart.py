from decimal import Decimal
from django.conf import settings
from shop.models import Product
from django.core.handlers.wsgi import WSGIRequest


class Cart(object):
    """Объект корзины"""
    def __init__(self, request: WSGIRequest) -> None:
        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart