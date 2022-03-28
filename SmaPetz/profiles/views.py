from django.shortcuts import render
from matplotlib.style import context
from .models import Profile, Pet, Pet_Lover, Store, Veterinarian, FriendRequest
from users.models import User
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from .forms import PetModelForm

# Create your views here.

def profile_test_view(request):
    if request.user.type == "PET":
        file_data = request.FILES or None
        profile = Pet.objects.get(user=request.user)
        form = PetModelForm(request.POST or None,file_data, instance=profile)
        confirm = False

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

        context = {
            'profile': profile
        }
        return render(request, 'profiles/vet_profile.html', {'profile':profile})

    elif request.user.type == "STORE":
        profile = Store.objects.get(user=request.user)

        context = {
            'profile': profile
        }
        return render(request, 'profiles/store_profile.html', {'profile':profile})

    elif request.user.type == "PET_LOVER":
        profile = Pet_Lover.objects.get(user=request.user)

        context = {
            'profile': profile
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