from django import forms
from .models import Pet, Veterinarian, Store, Pet_Lover

class PetModelForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = {'profilePic', 'bio', 'address', 'number','pet_type', 'breed', 'fish_type', 'reptile_type', 'bird_type', 'amphibian_type', 'mammal_type'}
        widgets = {
          'bio': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
          'address': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
          'breed': forms.Textarea(attrs={'rows':1, 'class':'form-control'}),
          'number': forms.Textarea(attrs={'rows':1, 'class':'form-control'}),
          'pet_type': forms.Select(attrs={'class': 'bootstrap-select'}),
          'fish_type': forms.Select(attrs={'class': 'bootstrap-select'}),
          'reptile_type': forms.Select(attrs={'class': 'bootstrap-select'}),
          'bird_type': forms.Select(attrs={'class': 'bootstrap-select'}),
          'amphibian_type': forms.Select(attrs={'class': 'bootstrap-select'}),
          'mammal_type': forms.Select(attrs={'class': 'bootstrap-select'}), 
        }

class VeterinarianModelForm(forms.ModelForm):
    class Meta:
        model = Veterinarian
        fields = {'profilePic', 'bio', 'address', 'number','education'}
        widgets = {
          'bio': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
          'address': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
          'education': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
          'number': forms.Textarea(attrs={'rows':1, 'class':'form-control'}),
        }

class StoreModelForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = {'profilePic', 'bio', 'address', 'number','store_type'}
        widgets = {
          'bio': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
          'address': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
          'number': forms.Textarea(attrs={'rows':1, 'class':'form-control'}),
          'store_type': forms.Select(attrs={'class': 'bootstrap-select'}),
        }

class PetLoverModelForm(forms.ModelForm):
    class Meta:
        model = Pet_Lover
        fields = {'profilePic', 'bio', 'address', 'number'}
        widgets = {
          'bio': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
          'address': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
          'number': forms.Textarea(attrs={'rows':1, 'class':'form-control'}),
        }

