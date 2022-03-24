import django
from django.shortcuts import render, redirect
from .models import Post, Reaction
from profiles.models import Pet, Profile, Veterinarian, Store, Pet_Lover, ProfileManager
from users.models import User
from .forms  import commentModelForm, postModelForm
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponseRedirect

# Create your views here.

def home_view(request):
    #query set to grab all the posts
    qs = Post.objects.all()
    if request.user.type == "PET":
        profile = Pet.objects.get(user=request.user)
        post =  Post.objects.filter(author = request.user)
        feed = Pet.feed_posts(self=request.user.pet)
        #feedprofile = Pet.objects.get(user=request.user.author)
        written = Post.objects.exclude(picture="")
        video = Post.objects.exclude(video="")

        #post form and comment form
        if request.method == 'POST':
            post_form = postModelForm()
            comment_form = commentModelForm()

            if 'post_form_submit' in request.POST:
                post_form = postModelForm(request.POST, request.FILES)
                if post_form.is_valid():
                    instance = post_form.save(commit=False)
                    instance.author = request.user 
                    instance.save() 
                return HttpResponseRedirect("/")

            if 'comment_form_submit' in request.POST:
                comment_form = commentModelForm(request.POST)
                if comment_form.is_valid():
                    instance = comment_form.save(commit = False)
                    instance.user = request.user
                    instance.post = Post.objects.get(id=request.POST.get('post_id'))
                    instance.save()
                return HttpResponseRedirect("/")
        else:
            post_form = postModelForm(request.POST or None)
            comment_form = commentModelForm(request.POST or None)



        context = {
            'qs': qs,
            'profile': profile,
            'post':post,
            'written':written,
            'feed':feed,
            'video':video,
            'post_form':post_form,
            'comment_form':comment_form
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


def reactions(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = User.object.get(user=request.user.likes)

        if profile in post_obj.liked_by.all():
            post_obj.liked_by.remove(profile)
        else:
            post_obj.liked_by.add(profile)

        love, angry, created = Reaction.objects.get(user=profile, post_id=post_id)

    return redirect('posts:home-view')



