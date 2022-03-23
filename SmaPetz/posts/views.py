from asyncio.windows_events import NULL
import django
from django.shortcuts import render
from .models import Post
from profiles.models import Pet, Profile, Veterinarian, Store, Pet_Lover, ProfileManager
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

def home_view(request):
    #query set to grab all the posts
    qs = Post.objects.all()
    if request.user.type == "PET":
        profile = Pet.objects.get(user=request.user)
        post =  Post.objects.filter(author = request.user)
        feed = Pet.feed_posts(self=request.user.pet)
        written = Post.objects.exclude(picture="")

        context = {
            'qs': qs,
            'profile': profile,
            'post':post,
            'written':written,
            'feed':feed
    }
    elif request.user.type == "PET_LOVER":
        profile = Veterinarian.objects.get(user=request.user)

        context = {
            'qs': qs,
            'profile': profile
    }
    elif request.user.type == "STORE":
        profile = Store.objects.get(user=request.user)

        context = {
            'qs': qs, 
            'profile': profile
    }
    elif request.user.type == "PET_LOVER":
        profile = Pet_Lover.objects.get(user=request.user)

        context = {
            'qs': qs, 
            'profile': profile
    }
    return render(request, 'posts/main.html', context)


