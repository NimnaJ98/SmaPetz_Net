from django import forms
from django.forms import fields
from .models import Post, Comment

class postModelForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('caption', 'picture', 'video', 'tags')
    widgets = {
      'caption': forms.Textarea(attrs={'rows':3,'cols':50, 'class':'form-control'}),
      'tags': forms.Textarea(attrs={'rows':1, 'cols':50, 'class':'form-control'}),
    }

class commentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Add a comment...', 'class':'form-control'}))
    class Meta:
          model = Comment
          fields = ('body',)
