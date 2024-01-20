# shopping_cart/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Cart, CartItem
from django.db import models
from django.http import JsonResponse

def product_list(request):
    products = Product.objects.all()
    
    # Tính tổng số lượng các CartItem và tổng tiền trong giỏ hàng
    total_products_in_cart = 0
    total_price_in_cart = 0
    cart_items = []

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.cartitem_set.all()
            total_products_in_cart = cart.cartitem_set.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
            
            # Tính tổng tiền cho mỗi CartItem và cập nhật vào trường subtotal
            for cart_item in cart_items:
                cart_item.subtotal = cart_item.product.price * cart_item.quantity
                total_price_in_cart += cart_item.subtotal
            
            # Cập nhật total_price_in_cart vào đối tượng Cart
            cart.total_price_in_cart = total_price_in_cart
            cart.save()

    return render(request, 'cart/product_list.html', {'products': products, 'total_products_in_cart': total_products_in_cart, 'cart_items': cart_items, 'total_price_in_cart': total_price_in_cart})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not cart_item_created:
        # Nếu sản phẩm đã có trong giỏ hàng, tăng số lượng
        cart_item.quantity += 1
        cart_item.save()

    # Tính tổng số lượng của từng sản phẩm trong giỏ hàng
    total_products_in_cart = CartItem.objects.filter(cart=cart).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    response_data = {
        'total_products_in_cart': total_products_in_cart
    }

    return JsonResponse(response_data)


# Trong views.py
from django.http import JsonResponse

def update_cart_item_quantity(request, item_id):
    action = request.GET.get('action', None)

    # Lấy đối tượng CartItem từ ID
    cart_item = get_object_or_404(CartItem, id=item_id)

    if action == 'increase':
        # Tăng số lượng sản phẩm
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        # Giảm số lượng sản phẩm
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        elif cart_item.quantity == 1:
            cart_item.quantity -= 1
            # Nếu giảm xuống 0, xóa sản phẩm khỏi giỏ hàng
            cart_item.delete()

    # Cập nhật tổng giá trị trong giỏ hàng
    cart = cart_item.cart
    cart_items = cart.cartitem_set.all()
    total_price_in_cart = sum(item.subtotal for item in cart_items)

    # Lưu thay đổi vào đối tượng Cart
    cart.save()

    # Tính toán các giá trị cần trả về
    response_data = {
        'quantity': cart_item.quantity,
        'subtotal': cart_item.subtotal,
        'total_price_in_cart': total_price_in_cart,
        'product_id': cart_item.product.id,
        'deleted': False,
    }

    # Nếu quantity = 0, đánh dấu là đã xóa
    if cart_item.quantity == 0:
        response_data['deleted'] = True
        response_data['quantity'] = 0

    return JsonResponse(response_data)


