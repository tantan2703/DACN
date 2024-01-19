# shopping_cart/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Cart
from django.http import JsonResponse

def product_list(request):
    products = Product.objects.all()
    return render(request, 'cart/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    
    total_products_in_cart = cart.products.count()
    
    response_data = {
        'total_products_in_cart': total_products_in_cart
    }
    
    return JsonResponse(response_data)