from django import forms
from .models import Pet, Veterinarian, Store, Pet_Lover

class PetModelForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = {'avatar', 'bio', 'address', 'number','pet_type', 'breed', 'fish_type', 'reptile_type', 'bird_type', 'amphibian_type', 'mammal_type'}