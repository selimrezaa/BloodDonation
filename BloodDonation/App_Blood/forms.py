from django import forms
from App_Blood.models import *


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'comm',
        'rows': 2,
        'cols': 40,
        'placeholder': "Enter  your Text here",
    }))

    class Meta:
        model = Comment
        fields = ['content']
