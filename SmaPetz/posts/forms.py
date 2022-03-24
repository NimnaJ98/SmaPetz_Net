from django import forms
from .models import Post, Comment

class postModelForm(forms.ModelForm):
      
    class Meta:
      model = Post
      fields = ('caption', 'picture', 'video', 'tags')
      widgets = {
        'caption': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
        'tags': forms.Textarea(attrs={'rows':1, 'class':'form-control'}),
      }
