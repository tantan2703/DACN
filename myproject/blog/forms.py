# forms.py
from django import forms
from .models import Comment
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, request=None, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.request = request
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            return None
        return content

