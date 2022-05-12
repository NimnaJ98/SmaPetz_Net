from django.shortcuts import render, redirect
from .models import Product

# Create your views here.

def store_view(request):
    newest_products = Product.objects.all()[0:8]
    context = {
        'newest_products': newest_products,
    }
    return render(request, 'products/store.html', context)

