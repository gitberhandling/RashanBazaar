from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'total': cart.get_total_price()
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
@require_POST
def cart_add(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        product = Product.objects.get(id=product_id, available=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart successfully',
            'total_items': cart.items.count()
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
def cart_remove(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return JsonResponse({
            'success': True,
            'message': 'Product removed from cart',
            'total_items': cart.items.count()
        })
    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found in cart'
        }, status=404)

@login_required
@require_POST
def cart_update(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
            
        return JsonResponse({
            'success': True,
            'message': 'Cart updated successfully',
            'total': cart.get_total_price(),
            'item_total': cart_item.get_cost() if quantity > 0 else 0
        })
    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found in cart'
        }, status=404)
