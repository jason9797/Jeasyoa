# -*- coding:utf-8 -*-
from django.contrib import admin
from models import Post, Category, Comments
from forms import PostForm, CommentsForm


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    form = PostForm


class CategoryAdmin(admin.ModelAdmin):
    pass


class CommentsAdmin(admin.ModelAdmin):
    form = CommentsForm


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)
