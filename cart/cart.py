from decimal import Decimal
from django.conf import settings
from shop.models import Product
from django.core.handlers.wsgi import WSGIRequest
# from coupons.models import Coupon
from typing import Union


class Cart(object):
    """Класс, описывающий корзину"""

    def __init__(self, request: WSGIRequest) -> None:
        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        # сохранение текущего примененного купона
        self.coupon_id = self.session.get('coupon_id')
        self.cart = cart

    def __iter__(self):
        """Перебирает элементы в корзине и получает продукты из базы данных"""
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:
        """Возвращает сумму количества всех товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product: Product, quantity: int = 1, update_quantity: bool = False) -> None:
        """Добавляет товар в корзину или увеличивает его количество на 1"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self) -> None:
        """Сохраняет корзины"""
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product: Product) -> None:
        """Удаляет товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self) -> Decimal:
        """Возвращает стоимость товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self) -> None:
        """Удаляет корзину из сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    # @property
    # def coupon(self) -> Union[Coupon, None]:
    #     """Если в корзине есть купон, возвращается купон с заданным id"""
    #     if self.coupon_id:
    #         return Coupon.objects.get(id=self.coupon_id)
    #     return None

    # def get_discount(self) -> Decimal:
    #     """Если в корзине есть купон, возвращается скидка, которая будет вычтена из общей суммы заказа"""
    #     if self.coupon:
    #         return (self.coupon.discount / Decimal('100')) * self.get_total_price()
    #     return Decimal('0')
    #
    # def get_total_price_after_discount(self) -> Decimal:
    #     """Возвращает общую сумму корзины после применения скидки"""
    #     return self.get_total_price() - self.get_discount()
