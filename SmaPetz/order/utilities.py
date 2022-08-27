from cart.cart import Cart
from .models import Order, OrderItem 


def checkout(request, first_name, last_name, email, phone, address1, address2, zipcode, country, amount):
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, address1=address1, address2=address2, zipcode=zipcode, country=country, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], store=item['product'].store, price=item['product'].price, quantity=item['quantity'])
        order.stores.add(item['product'].store)

    return order
        
