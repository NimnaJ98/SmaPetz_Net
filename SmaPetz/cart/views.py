from locale import currency
import logging
import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from .cart import Cart
from .forms import CheckoutForm
from order.utilities import checkout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_token = form.cleaned_data['stripe_token']
            try:
                charge = stripe.Charge.create(
                    amount=int(cart.get_total_cost() * 100),
                    currency='USD',
                    description='Charge from SmaPetz',
                    source=stripe_token
                )
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address1 = form.cleaned_data['address1']
                address2 = form.cleaned_data['address2']
                zipcode = form.cleaned_data['zipcode']
                country = form.cleaned_data['country']

                order = checkout(request, first_name, last_name, email, phone, address1, address2, zipcode, country, cart.get_total_cost())
                cart.clear()
                return redirect('cart:success')
            except Exception:
                messages.error(request, 'There was something wrong with the payment')

    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart:cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart:cart') 
        
    return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

@login_required
def success(request):
    return render(request, 'cart/success.html')