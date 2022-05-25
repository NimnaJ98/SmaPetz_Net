from django.shortcuts import redirect, render
from .cart import Cart

# Create your views here.

def cart_detail(request):
    cart = Cart(request)
    remove_from_cart = request.GET.get('remove_from_cart', '')
    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart:cart')
        
    return render(request, 'cart/cart.html')