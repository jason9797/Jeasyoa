# -*- coding:utf-8 -*-
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from account.models import User
from search_indexes import PostIndex
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(verbose_name=_('name'), unique=True, max_length=50)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        verbose_name_plural = _('Categorys')
        verbose_name = _('Category')
        # unique_together = ('name',)

    def __unicode__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(verbose_name=_('title'), max_length=50)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, verbose_name=_('Author'), null=True)
    category = models.ManyToManyField(Category, verbose_name=_('Category'))
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    allow = models.CharField(verbose_name=_('allow'), max_length=255, default='', blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Posts')
        verbose_name = _('Post')

    def get_absolute_url(self):
        return '/discussion/detail/%s' % self.pk

    def __unicode__(self):
        return self.title

    def get_post_perm(self, user):
        if 'u%su' % user.id not in self.allow:
            return False
        else:
            return True


class Comments(models.Model):
    content = RichTextUploadingField()
    post = models.ForeignKey(Post, verbose_name=_('Post'))
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_('Author'))

    class Meta:
        verbose_name_plural = _('Comments')
        verbose_name = _('Comment')

    def __unicode__(self):
        return '%s:%s' % (self.user.name, self.content)


def upindex_post(**kwargs):
    PostIndex().update_object(kwargs['instance'].post)
models.signals.post_save.connect(upindex_post, sender=Comments)
