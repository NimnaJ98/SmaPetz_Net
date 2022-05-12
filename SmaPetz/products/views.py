from django.shortcuts import render, redirect, get_object_or_404
import random
from .models import Product, Category

# Create your views here.

def store_view(request):
    newest_products = Product.objects.all()[0:8]
    context = {
        'newest_products': newest_products,
    }
    return render(request, 'products/store.html', context)

def product(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug= category_slug, slug=product_slug)
    similar_Products = list(product.category.products.exclude(id=product.id))

    if len(similar_Products) >= 4:
        similar_Products = random.sample(similar_Products, 4)
        
    context = {
        'product': product,
        'similar_Products':similar_Products,
    }
    return render(request, 'products/product.html', context)
    