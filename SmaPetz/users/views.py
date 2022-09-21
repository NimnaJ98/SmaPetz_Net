from cProfile import Profile
import profile
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from profiles.models import Veterinarian
from users.forms import UserRegistrationForm, UserLoginForm
from users.models import User
from products.models import Product
from posts.models import Post
import random
from django.db.models import Q
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Create your views here.
def home_view(request):
    return redirect('posts:home-view')

def vet_view(request):
    posts = Post.objects.all()
    vets = Veterinarian.objects.all()
    
    context = {
         'posts': posts,
         'vets':vets
    }
    return render(request, 'users/vet.html', context)

def searchVet(request):
    query = request.GET.get('query', '')
    words_in_query = word_tokenize(query)
    stop_words = set(stopwords.words("english"))
    filtered_list = []
    for w in words_in_query:
        if w.casefold() not in stop_words:
            filtered_list.append(w)

    for word in filtered_list:
        posts = Post.objects.filter(Q(caption__icontains=word) | Q(tags__icontains=word))
        profiles = Veterinarian.objects.filter(Q(address__icontains=word) | Q(bio__icontains=word) | Q(slug__icontains=word))
    
    context = {
        'query':query,
        'word':word,
        'posts':posts,
        'profiles':profiles, 
    }
    return render(request, 'users/vet_search.html', context)

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