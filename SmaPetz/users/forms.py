from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'type', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control custom-class'}),
            'name': forms.TextInput(attrs={'class':'form-control custom-class'}),
       }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class':'form-control custom-class'})
        self.fields['password1'].widget.attrs.update({'class':'form-control custom-class'})
        self.fields['password2'].widget.attrs.update({'class':'form-control custom-class'})

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class':'form-control custom-class'}))

    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control custom-class'}),
        }

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Credentials")

