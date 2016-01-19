# -*- coding:utf-8 -*-
# __author__ = 'jason_lee'
import datetime
from haystack import indexes
import discussion.models


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='content', document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    # author = indexes.CharField(model_attr='author__username')
    created = indexes.DateTimeField(model_attr='created')
    comments = indexes.MultiValueField()

    def get_model(self):
        return discussion.models.Post

    def prepare_comments(self, obj):
        # Since we're using a M2M relationship with a complex lookup,
        # we can prepare the list here.
        return [comments.content for comments in obj.comments_set.all().order_by('-created')]

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

# class CommentIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(model_attr='content', document=True, use_template=True)
#
#     def get_model(self):
#         return Comments
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.filter(created__lte=datetime.datetime.now())
