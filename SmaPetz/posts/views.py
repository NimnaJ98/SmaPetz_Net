from django.contrib import messages
import django
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post
from profiles.models import Pet, Profile, Veterinarian, Store, Pet_Lover
from django.shortcuts import render
from .forms  import commentModelForm, postModelForm
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, DeleteView


# Create your views here.
def home_view(request):
    #query set to grab all the posts
    post =  Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    written = Post.objects.exclude(picture="")
    video = Post.objects.exclude(video="")

    #post form and comment form
     #Post and Comment Forms
    post_form = postModelForm()
    comment_form = commentModelForm()
    post_added = False

    profile = Profile.objects.get(user=request.user)

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
        
    }

    return render(request, 'posts/main.html', context)
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:home-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it.')
        return obj

class PostUpdateView(UpdateView):
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
