# cart/admin.py
from django.contrib import admin
from .models import Product
from .models import Cart, CartItem

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

admin.site.register(Cart)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Product)
