from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment


User = get_user_model()


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                }
            )
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
