from multiprocessing import context
from django.shortcuts import render
from .models import Post

# Create your views here.

def home_view(request):

    #query set to grab all the posts
    qs = Post.objects.all()
    context = {
        'hello': 'hello world',
        'qs': qs
    }
    return render(request, 'posts/main.html', context)