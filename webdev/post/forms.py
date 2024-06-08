from django_summernote.widgets import SummernoteWidget
from django import forms

from .models import Comment, Post, Tag


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }


# class TagForm(forms.ModelForm):
#
#     class Meta:
#         model = Tag
#         fields = ['name']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'cat', 'body', 'title_image', 'tags']
        widgets = {
            'body': SummernoteWidget(),
        }


class SearchForm(forms.Form):
    query = forms.CharField(label='Введите запрос')
