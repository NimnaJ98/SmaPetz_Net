from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from users.forms import UserRegistrationForm, UserLoginForm
from users.models import User
from products.models import Product
from posts.models import Post
import random


# Create your views here.
def home_view(request):
    return redirect('posts:home-view')

def about_view(request):
    products = list(Product.objects.all())
    show_Products = random.sample(products, 8)
    posts = list(Post.objects.exclude(picture=""))
    show_posts = random.sample(posts, 6)
    
    context = {
        'show_Products': show_Products,
        'show_posts': show_posts,
    }
    return render(request, 'users/about.html', context)

def register(request):
    context = {}
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        context['register_form'] = form
    
    else:
        form = UserRegistrationForm()
        context['register_form'] = form
    
    return render(request, 'users/register.html', context)


def login_view(request):
    context = {}
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, email=email, password = password)

            if user is not None:
                login(request, user)
                return redirect("users:dashboard")

        else:
            context['login_form'] = form

    else:
        form = UserLoginForm()
        context["login_form"] = form

    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('users:login')