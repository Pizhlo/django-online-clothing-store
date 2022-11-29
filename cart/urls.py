from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.cart_detail, name='cart_detail'),
    re_path(r'^add/(?P<product_id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    re_path(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]