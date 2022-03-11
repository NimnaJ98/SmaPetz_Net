from django.contrib import admin
from .models import Profile, Pet, Veterinarian, Store, Pet_Lover

# Register your models here.


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
     readonly_fields = ['usertype']
     if Pet.pet_type == "FISH":
          readonly_fields = ['reptile_type','bird_type','amphibian_type','mammal_type']
     elif Pet.pet_type == "REPTILE":
          readonly_fields = ['fish_type','bird_type','amphibian_type','mammal_type']
     elif Pet.pet_type == "BIRD":
          readonly_fields = ['fish_type','reptile_type','amphibian_type','mammal_type']
     elif Pet.pet_type == "AMPHIBIAN":
          readonly_fields = ['fish_type','reptile_type','bird_type','mammal_type']
     elif Pet.pet_type == "MAMMAL":
          readonly_fields = ['fish_type','reptile_type','bird_type','amphibian_type']
     
     

@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
     readonly_fields = ['usertype']

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
     readonly_fields = ['usertype']

@admin.register(Pet_Lover)
class PetLoverAdmin(admin.ModelAdmin):
     readonly_fields = ['usertype']

