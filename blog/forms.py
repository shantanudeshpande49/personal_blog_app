from django import forms 
from . models import Comment

class CommentForm(forms.ModelForm):    
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            'userName': 'Your Name',
            'userEmail': 'Your Email',
            'text': 'Your Comment'
        }

