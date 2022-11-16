from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path('detail/<int:product_id>/<str:product_slug>/', product_detail, name='product_detail'),
    path('category/<str:slug>/', product_list_by_category, name='product_list_by_category'),
]
