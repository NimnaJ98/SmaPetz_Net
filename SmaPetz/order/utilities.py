from itertools import product
from cart.cart import Cart
from .models import Order, OrderItem 


def checkout(request, first_name, last_name, email, address1, address2, zipcode, country, phone, amount):
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, address1=address1, address2=address2, zipcode=zipcode, country=country, phone=phone, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], srore=item['product'].store, price=item['product'].price, quantity=item['quantity'])
        order.stores.add(item['product'].store)

    return order
        
