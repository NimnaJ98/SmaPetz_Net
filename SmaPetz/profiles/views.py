from django.shortcuts import render
from .models import Profile, Pet, Pet_Lover, Store, Veterinarian, FriendRequest
from users.models import User
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from .forms import PetLoverModelForm, PetModelForm, StoreModelForm, VeterinarianModelForm

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
    if request.user.type == 'PET':
        profile = Pet.objects.get(user=request.user)
    elif request.user.type == 'VET':
        profile = Veterinarian.objects.get(user=request.user)
    elif request.user.type == 'STORE':
        profile = Store.objects.get(user=request.user)
    elif request.user.type == 'PET_LOVER':
        profile = Pet_Lover.objects.get(user=request.user)
    qs = FriendRequest.objects.invitationsReceived(request.user)

    context ={'qs':qs}

    return render(request, 'profiles/my_requests.html', context)

def profile_list_view(request):
    user = request.user
    if request.user.type == 'PET':
        qs = Pet.objects.get_all_profiles(user)
    elif request.user.type == 'VET':
        qs = Veterinarian.objects.get_all_profiles(user)
    elif request.user.type == 'STORE':
        qs = Store.objects.get_all_profiles(user)
    elif request.user.type == 'PET_LOVER':
        qs = Pet_Lover.objects.get_all_profiles(user)
    context ={'qs':qs}

    return render(request, 'profiles/profile_list.html', context)