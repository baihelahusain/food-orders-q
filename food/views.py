from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item, Cart, Order, OrderItem
from django.template import loader
from .forms import ItemForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Sum, F
from decimal import Decimal

# Function to check if user is a superuser
def is_superuser(user):
    return user.is_superuser

# Create your views here.
def index(request):
    item_list = Item.objects.all()
    template = loader.get_template("food/index.html")
    context = {
        'item_list': item_list, 
    }
    return render(request, "food/index.html", context)
       
def item(request):
    return HttpResponse("HEllo")

def detail(request, item_id):
    item = Item.objects.get(pk=item_id)
    context ={
        'item':item,
    }
    return render(request, "food/detail.html", context)

@login_required
@user_passes_test(is_superuser)
def create_item(request):
    if not request.user.is_superuser:
        raise PermissionDenied("You don't have permission to add items")
    
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('food:index')
    return render(request, 'food/item-form.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def update_item(request,id):
    if not request.user.is_superuser:
        raise PermissionDenied("You don't have permission to update items")
    
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('food:index')
    return render(request, 'food/item-form.html', {'form': form, 'item': item})

@login_required
@user_passes_test(is_superuser)
def delete_item(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied("You don't have permission to delete items")
    
    item = Item.objects.get(id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('food:index')
    return render(request, 'food/item-delete.html', {'item': item})

# Cart functionality
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f"{item.Item_name} added to your cart!")
    return redirect('food:index')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'food/cart.html', context)

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, user=request.user, item_id=item_id)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            messages.info(request, f"{cart_item.item.Item_name} removed from cart")
            return redirect('food:view_cart')
    
    cart_item.save()
    return redirect('food:view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, user=request.user, item_id=item_id)
    cart_item.delete()
    messages.info(request, f"{cart_item.item.Item_name} removed from cart")
    return redirect('food:view_cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('food:view_cart')
    
    total_price = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        # Get form data
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        
        # Create new order
        order = Order.objects.create(
            user=request.user,
            total_price=Decimal(total_price)
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                price=Decimal(cart_item.item.Item_price)
            )
        
        # Update user profile with delivery address if provided
        if address and hasattr(request.user, 'profile'):
            profile = request.user.profile
            profile.location = address
            profile.save()
        
        # Clear the cart
        cart_items.delete()
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect('food:order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'total': total_price
    }
    return render(request, 'food/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'food/order_confirmation.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'food/order_history.html', context)

# Superuser order management views
@login_required
@user_passes_test(is_superuser)
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'food/all_orders.html', context)

@login_required
@user_passes_test(is_superuser)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES).keys():
            order.status = status
            order.save()
            messages.success(request, f"Order status updated to {order.get_status_display()}")
        
    context = {
        'order': order,
        'order_items': order_items,
        'status_choices': Order.STATUS_CHOICES
    }
    return render(request, 'food/order_detail.html', context)