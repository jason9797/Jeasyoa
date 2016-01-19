# -*- coding:utf-8 -*-
from models import Post
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django.views.generic import View
from django.utils.translation import ugettext as _


def post_detail_permission(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        detail_id = kwargs["pk"]
        post = get_object_or_404(Post, pk=detail_id)
        if not post.get_post_perm(request.user):
            return HttpResponse("<script language='javascript'>\
            alert('%s!');window.history.go(-1);</script>" % _('no permission'))
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func


class PostDetailPermissionMixin(View):
    @method_decorator(post_detail_permission)
    def dispatch(self, *args, **kwargs):
        return super(PostDetailPermissionMixin, self).dispatch(*args, **kwargs)
