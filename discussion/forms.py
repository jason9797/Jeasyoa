# -*- coding:utf-8 -*-
from django import forms
from ckeditor.widgets import CKEditorWidget
from models import Post, Comments


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'allow')
        widgets = {
            'category': forms.CheckboxSelectMultiple
        }


class CommentsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Comments
        fields = ('content',)
