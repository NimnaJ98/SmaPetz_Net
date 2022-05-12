import imp
from django.shortcuts import render, redirect, get_object_or_404
import random
from .models import Product, Category
from posts.models import Post
from django.db.models import Q

# Create your views here.
def searchProduct(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    posts = Post.objects.filter(Q(caption__icontains=query) | Q(tags__icontains=query))
    context = {
        'products': products,
        'query':query,
        'posts':posts,
    }
    return render(request, 'products/productSearch.html', context)


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

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    context = {
        'category': category,
    }
    return render(request, 'products/category.html', context)