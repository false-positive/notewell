from django import forms
from django.db.models import fields
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']