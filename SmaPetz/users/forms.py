from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'type', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control register'}),
            'name': forms.TextInput(attrs={'class':'form-control register'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control pwd'})
        }

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Credentials")

