from django.shortcuts import render
from .models import Profile, Pet, Pet_Lover, Store, Veterinarian
from users.models import User


# Create your views here.


def profile_test_view(request):
    if request.user.type == "PET":
        profile = Pet.objects.get(user=request.user)
        return render(request, 'profiles/pet_profile.html', {'profile':profile})
    
    elif request.user.type == "VET":
        profile = Veterinarian.objects.get(user=request.user)
        return render(request, 'profiles/vet_profile.html', {'profile':profile})

    elif request.user.type == "STORE":
        profile = Store.objects.get(user=request.user)
        return render(request, 'profiles/store_profile.html', {'profile':profile})

    elif request.user.type == "PET_LOVER":
        profile = Veterinarian.objects.get(user=request.user)
        return render(request, 'profiles/petLover_profile.html', {'profile':profile})