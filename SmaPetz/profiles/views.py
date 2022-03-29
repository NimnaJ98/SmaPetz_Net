from django.shortcuts import render
from flask import request
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

# doesnt work
def profiles_to_request(request):
    user = request.user
    if request.user.type == 'PET':
        qs = Pet.objects.get_profiles_to_request(user)
    elif request.user.type == 'VET':
        qs = Veterinarian.objects.get_profiles_to_request(user)
    elif request.user.type == 'STORE':
        qs = Store.objects.get_profiles_to_request(user)
    elif request.user.type == 'PET_LOVER':
        qs = Pet_Lover.objects.get_profiles_to_request(user)
    context ={'qs':qs}

    return render(request, 'profiles/to_request.html', context)


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

class ProfileList(ListView):
    model = Pet, Veterinarian, Store, Pet_Lover
    template_name = 'profiles/profile_list.html'
    context_object_name ='qs'

    def get_queryset(self) :
        if self.request.user.type == 'PET':
            qs = Pet.objects.get_all_profiles(self.request.user)
        if self.request.user.type == 'VET':
            qs = Veterinarian.objects.get_all_profiles(self.request.user)
        if self.request.user.type == 'STORE':
            qs = Store.objects.get_all_profiles(self.request.user)
        if self.request.user.type == 'PET_LOVER':
            qs = Pet_Lover.objects.get_all_profiles(self.request.user)
        return qs
    
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        user = User.objects.get(email__iexact=self.request.user)
        if self.request.user.type == 'PET':
            profile = Pet.objects.get(user=user)
        if self.request.user.type == 'VET':
            profile = Veterinarian.objects.get(user=user)
        if self.request.user.type == 'STORE':
            profile = Store.objects.get(user=user)
        if self.request.user.type == 'PET_LOVER':
            profile = Pet_Lover.objects.get(user=user)

        request_receiver = FriendRequest.objects.filter(sender=self.user)
        request_sender = FriendRequest.objects.filter(receiver=self.user)

        request_receiverList =[]
        request_senderList =[]

        for item in request_receiver:
            request_receiverList.append(item.receiver.user)
        for item in request_sender:
            request_senderList.append(item.sender.user)
        
        context["request_receiverList"] = request_receiverList
        context["request_senderList"] = request_senderList
        
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context