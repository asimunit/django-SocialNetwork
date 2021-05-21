from django import forms
from .models import Post


class NewPostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

    class Meta:
        model = Post
        fields = ['description']
