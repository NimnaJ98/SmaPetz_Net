import imp
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import random
from django.contrib.auth.decorators import login_required
import cart
from .models import Product, Category
from profiles.models import Store, Profile
from posts.models import Post
from cart.cart import Cart
from .forms import AddToCartForm
from django.db.models import Q

# Create your views here.
def searchProduct(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    posts = Post.objects.filter(Q(caption__icontains=query) | Q(tags__icontains=query))
    profiles = Profile.objects.filter(Q(address__icontains=query) | Q(bio__icontains=query))
    context = {
        'products': products,
        'query':query,
        'posts':posts,
        'profiles':profiles, 
    }
    return render(request, 'products/productSearch.html', context)


def store_view(request):
    newest_products = Product.objects.all()[0:12]
    stores = Store.objects.all()
    list_stores = list(stores)

    if len(list_stores) >= 4:
        list_stores = random.sample(list_stores, 4)
    
    context = {
        'newest_products': newest_products,
        'stores':stores
    }
    return render(request, 'products/store.html', context)

@login_required
def product(request, category_slug, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, category__slug= category_slug, slug=product_slug)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)
            messages.success(request, 'The product was added to the cart')
            return redirect('products:product', category_slug=category_slug, product_slug=product_slug)

    else:
        form = AddToCartForm()

    similar_Products = list(product.category.products.exclude(id=product.id))

    if len(similar_Products) >= 4:
        similar_Products = random.sample(similar_Products, 4)
        
    context = {
        'product': product,
        'similar_Products':similar_Products,
        'form':form
    }
    return render(request, 'products/product.html', context)

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    context = {
        'category': category,
    }
    return render(request, 'products/category.html', context)