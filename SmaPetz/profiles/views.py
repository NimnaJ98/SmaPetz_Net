from django.shortcuts import render
from .models import Profile, Pet, Pet_Lover, Store, Veterinarian, FriendRequest
from users.models import User
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from .forms import PetLoverModelForm, PetModelForm, StoreModelForm, VeterinarianModelForm
from django.views.generic import ListView

# Create your views here.

def profile_test_view(request):
    file_data = request.FILES or None
    confirm = False
    if request.user.type == "PET":
        profile = Pet.objects.get(user=request.user)
        form = PetModelForm(request.POST or None,file_data, instance=profile)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                confirm = True

        context = {
            'profile': profile,
            'form':form,
            'confirm':confirm,
        }
        return render(request, 'profiles/pet_profile.html', context)

    elif request.user.type == "VET":
        profile = Veterinarian.objects.get(user=request.user)
        form = VeterinarianModelForm(request.POST or None,file_data, instance=profile)

        context = {
            'profile': profile,
            'form':form,
            'confirm':confirm,
        }
        return render(request, 'profiles/vet_profile.html', {'profile':profile})

    elif request.user.type == "STORE":
        profile = Store.objects.get(user=request.user)
        form = StoreModelForm(request.POST or None,file_data, instance=profile)

        context = {
            'profile': profile,
            'form':form,
            'confirm':confirm,
        }
        return render(request, 'profiles/store_profile.html', {'profile':profile})

    elif request.user.type == "PET_LOVER":
        profile = Pet_Lover.objects.get(user=request.user)
        form = PetLoverModelForm(request.POST or None,file_data, instance=profile)

        context = {
            'profile': profile,
            'form':form,
            'confirm':confirm,
        }
        return render(request, 'profiles/petLover_profile.html', {'profile':profile})


def received_requests_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = FriendRequest.objects.invitationsReceived(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results)==0:
        is_empty = True
        
    context = {
        'qs': results,
        'is_empty':is_empty, 
        }

    return render(request, 'profiles/my_invites.html', context)

