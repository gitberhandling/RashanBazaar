from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cart.models import Cart
from .models import Order, OrderItem

# Create your views here.

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_create(request):
    cart = Cart.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Create the order
        try:
            order = Order.objects.create(
                user=request.user,
                address_line1=request.POST.get('address_line1'),
                address_line2=request.POST.get('address_line2', ''),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                postal_code=request.POST.get('postal_code'),
                phone=request.POST.get('phone'),
                payment_method=request.POST.get('payment_method', 'cod'),
                total_amount=cart.get_total_price()
            )
            
            # Create order items from cart items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            
            # Clear the cart
            cart.items.all().delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('orders:order_detail', order_id=order.id)
        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}')
            return redirect('orders:order_create')
    
    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'total': cart.get_total_price()
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_track(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_track.html', {'order': order})

@login_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    
    return redirect('orders:order_detail', order_id=order.id)
