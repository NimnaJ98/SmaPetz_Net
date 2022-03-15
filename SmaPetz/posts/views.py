import django
from django.shortcuts import render
from .models import Post
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

def home_view(request):
    #query set to grab all the posts
    context = {
        'hello': 'hello world',
        
    }
    return render(request, 'posts/main.html', context)

def post_view_json(request):
    qs = Post.objects.all()
    data = serializers.serialize('json', qs)
    return JsonResponse({'data':data})