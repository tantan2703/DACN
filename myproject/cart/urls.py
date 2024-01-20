# shopping_cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
        path('update_cart_item_quantity/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
]