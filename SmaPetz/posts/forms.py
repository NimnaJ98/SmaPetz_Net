from django import forms
from .models import Post, Comment

class postModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption', 'picture', 'video', 'tags')