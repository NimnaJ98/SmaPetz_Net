from django import forms
from django_countries.fields import CountryField



class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address1 = forms.CharField(max_length=255)
    address2 = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    country = CountryField().formfield()
    stripe_token = forms.CharField(max_length=255)