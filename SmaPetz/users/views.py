from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from users.forms import UserRegistrationForm, UserLoginForm



# Create your views here.
def feed_view(request):
    return render(request, 'posts/main.html')

def register(request):
    context = {}
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
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
            user = authenticate(request, enail=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('feed')

    else:
        form = UserLoginForm()
        context['login_form'] = form

    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')