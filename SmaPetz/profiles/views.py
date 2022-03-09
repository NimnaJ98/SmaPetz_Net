from django.shortcuts import render
from .models import Profile, Pet, Pet_Lover, Store, Veterinarian
from users.models import User
from django.views.generic import TemplateView, View
from django.http import JsonResponse



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
        profile = Pet_Lover.objects.get(user=request.user)
        return render(request, 'profiles/petLover_profile.html', {'profile':profile})


class UserProfileView(TemplateView):
    template_name = 'profiles/user_profile.html'

class UserProfileData(View):
    def get(self, *args, **kwargs):
        if self.user.type == "PET":
            profile = Pet.objects.get(user=self.user)
        elif self.user.type == "VET":
            profile = Veterinarian.objects.get(user=self.user)
            
        elif self.user.type == "STORE":
            profile = Store.objects.get(user=self.user)

        elif self.user.type == "PET_LOVER":
            profile = Pet_Lover.objects.get(user=self.user)

        qsPet = profile.get_Petfollow_suggestions()
        qsVet = profile.get_Vetfollow_suggestions()
        qsStore = profile.get_Storefollow_suggestions()
        qsPetLover = profile.get_PetLoverfollow_suggestions()
        profiles_to_follow = []
        for pet in qsPet:
            p = Pet.objects.get(user__username =pet.name)
            petProfile_item = {
                'id':p.id,
                'user':p.pet.name,
                'avatar' : p.avatar.url
            }
            profiles_to_follow.append(petProfile_item)
            for vet in qsVet:
                v = Veterinarian.objects.get(user__username = vet.name)
            vetProfile_item = {
                'id':v.id,
                'user':v.vet.name,
                'avatar' : v.avatar.url
            }
            profiles_to_follow.append(vetProfile_item)
            for store in qsStore:
                s = Store.objects.get(user__username = store.name)
            vetProfile_item = {
                'id':s.id,
                'user':s.store.name,
                'avatar' : s.avatar.url
            }
            profiles_to_follow.append(vetProfile_item)
            for lover in qsPetLover:
                l = Pet_Lover.objects.get(user__username = lover.name)
            vetProfile_item = {
                'id':l.id,
                'user':l.lover.name,
                'avatar' : l.avatar.url
            }
            profiles_to_follow.append(vetProfile_item)
            

        return JsonResponse ({'pf_data': profiles_to_follow})
