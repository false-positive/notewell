from django import forms
from django.db.models import fields
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)

        self.fields['content'].widget.attrs['rows'] = '3'
        self.fields['content'].widget.attrs['placeholder'] = 'Post a comment...'