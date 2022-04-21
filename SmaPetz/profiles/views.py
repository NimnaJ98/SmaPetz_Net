from re import L
from unittest import result
from django.dispatch import receiver
from django.shortcuts import redirect, render, get_object_or_404
from .models import Profile, Pet, Pet_Lover, Store, Veterinarian, FriendRequest
from users.models import User
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from .forms import PetLoverModelForm, PetModelForm, StoreModelForm, VeterinarianModelForm
from django.views.generic import ListView, DetailView
from posts.models import Post
from django.db.models import Q


# Create your views here.
def profile_test_view(request):
    
    confirm = False
    profile = Profile.objects.get(user=request.user)
    post =  Post.objects.all()
    photo = Post.objects.exclude(picture="")
    video = Post.objects.exclude(video="")

    if request.user.type == "PET":
       
        pet = Pet.objects.get(user=request.user)
        pet_form = PetModelForm(request.POST or None,request.FILES or None, instance=profile)

        if request.method == 'POST':
            if pet_form.is_valid():
                pet_form.save()
                confirm = True
            return redirect('profiles:profile-test')

        context = {
            'profile': profile,
            'pet_form':pet_form,
            'confirm':confirm,
            'pet':pet,
            'post':post,
            'photo':photo,
            'video':video
        }
        return render(request, 'profiles/pet_profile.html', context)

    elif request.user.type == "VET":
        vet = Veterinarian.objects.get(user=request.user)
        vet_form = VeterinarianModelForm(request.POST or None,request.FILES or None, instance=profile)

        if request.method == 'POST':
            if vet_form.is_valid():
                vet_form.save()
                confirm = True
            return redirect('profiles:profile-test')

        context = {
            'profile': profile,
            'vet_form':vet_form,
            'confirm':confirm,
            'vet':vet,
            'post':post,
            'photo':photo,
            'video':video
        }
        return render(request, 'profiles/vet_profile.html', context)

    elif request.user.type == "STORE":
        store = Store.objects.get(user=request.user)
        store_form = StoreModelForm(request.POST or None,request.FILES or None, instance=profile)

        if request.method == 'POST':
            if store_form.is_valid():
                store_form.save()
                confirm = True
            return redirect('profiles:profile-test')

        context = {
            'profile': profile,
            'store_form':store_form,
            'confirm':confirm,
            'store':store,
            'post':post,
            'photo':photo,
            'video':video
        }
        return render(request, 'profiles/store_profile.html', context)

    elif request.user.type == "PET_LOVER":
        lover = Pet_Lover.objects.get(user=request.user)
        lover_form = PetLoverModelForm(request.POST or None,request.FILES or None, instance=profile)

        if request.method == 'POST':
            if lover_form.is_valid():
                lover_form.save()
                confirm = True
            return redirect('profiles:profile-test')

        context = {
            'profile': profile,
            'lover_form':lover_form,
            'confirm':confirm,
            'lover':lover,
            'post':post,
            'photo':photo,
            'video':video
        }
        return render(request, 'profiles/petLover_profile.html', context)

#to display the received friend requests of the logged in user
def received_requests_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = FriendRequest.objects.received_requests(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) ==0:
        is_empty = True

    context = {
        'qs':results,
        'is_empty':is_empty,
        }

    return render(request, 'profiles/received_requests.html', context)

#accept received requests
def accept_requests(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user = request.user)

        friendship = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)
        if friendship.status == 'send':
            friendship.status = 'accepted'
            friendship.save()

    return redirect('profiles:received-requests')

#reject received requests
def reject_requests(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user = request.user)

        friendship = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)
        friendship.delete()
    return redirect('profiles:received-requests')

#to display the profiles available to request
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_profiles_to_send_requests(user)

    context = {'qs':qs}

    return render(request, 'profiles/to_request.html', context)

#to display all the profiles except for the logged in user
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs':qs}

    return render(request, 'profiles/profile_list.html', context)

#class-based view to display profiles
class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(email__iexact = self.request.user)
        profile = Profile.objects.get(user = user)

        req_receiver = FriendRequest.objects.filter(sender=profile)
        req_sender = FriendRequest.objects.filter(receiver=profile)

        request_receiver = []
        request_sender = []

        for item in req_receiver:
            request_receiver.append(item.receiver.user)
        for item in req_sender:
            request_sender.append(item.sender.user)
        context["request_receiver"] = request_receiver
        context["request_sender"] = request_sender

        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

#send friend requests to profiles
def send_requests(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        friendship = FriendRequest.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:profile-test')

#remove friends
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        friendship = FriendRequest.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        friendship.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('profiles:profile-test')