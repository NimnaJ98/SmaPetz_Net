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
    if request.user.type == "PET":
       
        pet = Pet.objects.get(user=request.user)
        form = PetModelForm(request.POST or None,request.FILES or None, instance=profile)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                confirm = True

        context = {
            'profile': profile,
            'form':form,
            'confirm':confirm,
            'pet':pet
        }
        return render(request, 'profiles/pet_profile.html', context)

    elif request.user.type == "VET":
        profile = Veterinarian.objects.get(user=request.user)
        form = VeterinarianModelForm(request.POST or None,request.FILES or None, instance=profile)

        context = {
            'profile': profile,
            'form':form,
            'confirm':confirm,
        }
        return render(request, 'profiles/vet_profile.html', {'profile':profile})

    elif request.user.type == "STORE":
        profile = Store.objects.get(user=request.user)
        form = StoreModelForm(request.POST or None,request.FILES or None, instance=profile)

        context = {
            'profile': profile,
            'form':form,
            'confirm':confirm,
        }
        return render(request, 'profiles/store_profile.html', {'profile':profile})

    elif request.user.type == "PET_LOVER":
        lover = Pet_Lover.objects.get(user=request.user)
        petLoverform = PetLoverModelForm(request.POST or None,request.FILES or None, instance=profile)

        context = {
            'profile': profile,
            'petLoverform':petLoverform,
            'confirm':confirm,
            'lover':lover
        }
        return render(request, 'profiles/petLover_profile.html', {'profile':profile})

#to display the received friend requests of the logged in user
def received_requests_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = FriendRequest.objects.received_requests(profile)

    context = {'qs':qs}

    return render(request, 'profiles/received_requests.html', context)

#to display all the profiles except for the logged in user
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs':qs}

    return render(request, 'profiles/profile_list.html', context)

def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_profiles_to_send_requests(user)

    context = {'qs':qs}

    return render(request, 'profiles/to_request.html', context)


def accept_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')

def reject_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')

def send_invitations(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = FriendRequest.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:profile_test_view')

def remove_from_friends(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
    
        rel = FriendRequest.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:profile_test_view')