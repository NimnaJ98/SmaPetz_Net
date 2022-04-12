from django.contrib import messages
import django
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Like
from profiles.models import Pet, Profile, Veterinarian, Store, Pet_Lover
from django.shortcuts import render
from .forms  import commentModelForm, postModelForm
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required
def home_view(request):
    #query set to grab all the posts
    post =  Post.objects.all()
    profile = Profile.objects.get(user=request.user)    
    written = Post.objects.exclude(picture="")
    video = Post.objects.exclude(video="")

    #Post and Comment Forms
    post_form = postModelForm()
    comment_form = commentModelForm()
    post_added = False

    if 'post_form_submit' in request.POST:
        print(request.POST)
        post_form = postModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = postModelForm()
            post_added = True

    if 'comment_form_submit' in request.POST:
        comment_form = commentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            comment_form = commentModelForm()


    context = {
        'profile': profile,
        'post':post,
        'written':written,
        'video':video,
        'post_form':post_form,
        'comment_form':comment_form,
        'post_added': post_added,
    }

    return render(request, 'posts/main.html', context)

@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id = post_id)
        profile = Profile.objects.get(user = user)

        if profile in post_obj.liked_by.all():
            post_obj.liked_by.remove(profile)
        else:
            post_obj.liked_by.add(profile)

        like, created = Like.objects.get_or_create(user = profile, post_id = post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

            post_obj.save()
            like.save()
    return redirect('posts:home-view')
        

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:home-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it.')
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = postModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url= reverse_lazy('posts:home-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)

        else:
            form.add_error(None, "You need to be the author of the post in order to update it.")
            return super().form_invalid(form)
