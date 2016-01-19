# -*- coding:utf-8 -*-
# from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, FormView, DeleteView, TemplateView, UpdateView
from forms import CommentsForm, PostForm
from django.shortcuts import HttpResponseRedirect, HttpResponse, Http404
from haystack.generic_views import SearchView
from models import Post, Comments, Category
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from mixin import PostDetailPermissionMixin
from django.contrib import messages
from django.core import serializers
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
import datetime
from account.models import User
# from search_indexes import PostIndex
# Create your views here.


class DiscussionList(ListView):

    template_name = 'discussion_list.html'
    model = Post
    queryset = Post.objects.all().order_by('-created')
    paginate_by = 10

    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, *args, **kwargs):
        return super(DiscussionList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiscussionList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        if self.request.GET.get("category"):
            object_list = self.model.objects.filter(
                category__name=self.request.GET.get("category")).filter(
                allow__icontains='u%su' % self.request.user.id).order_by('-created')
        else:
            object_list = self.model.objects.filter(
                allow__icontains='u%su' % self.request.user.id).order_by('-created')
        return object_list


class DiscussionCreate(CreateView):

    form_class = PostForm
    template_name = 'discussion_new.html'

    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, *args, **kwargs):
        return super(DiscussionCreate, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        kwargs['allow'] = 'u%su,' % request.user.id + ','.join(['u'+i+'u' for i in request.POST.getlist("allow_user")])
        kwargs['author'] = request.user
        kwargs['content'] = request.POST.get("content")
        kwargs['title'] = request.POST.get("title")
        if request.POST.get("content") and request.POST.get("title"):
            category = request.POST.getlist("category")
            post = Post.objects.create(**kwargs)
            post.category.add(*category)
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            if not request.POST.get("title"):
                messages.add_message(self.request, messages.ERROR, _('title is required'))
            if not request.POST.get("content"):
                messages.add_message(self.request, messages.ERROR, _('content is required'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DiscussionDetail(PostDetailPermissionMixin, DetailView):

    template_name = 'discussion_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(DiscussionDetail, self).get_context_data(**kwargs)
        context['conmentform'] = CommentsForm
        return context


class DiscussionUpdate(UpdateView):
    form_class = PostForm
    template_name = 'discussion_update.html'
    model = Post

    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, *args, **kwargs):
        return super(DiscussionUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiscussionUpdate, self).get_context_data(**kwargs)
        context['allow_user_list'] = [int(i.replace('u', '')) for i in self.object.allow.split(',') if i]
        allow_department_list = []
        for i in context['allow_user_list']:
            try:
                for k in User.objects.get(pk=i).departments.all():
                    allow_department_list.append(k.id)
            except ObjectDoesNotExist:
                continue
        allow_department_list = list(set(allow_department_list))
        context['allow_department_list'] = allow_department_list
        return context

    def post(self, request, *args, **kwargs):
        kwargs['allow'] = 'u%su,' % request.user.id + ','.join(['u'+i+'u' for i in request.POST.getlist("allow_user")])
        kwargs['author'] = request.user
        kwargs['content'] = request.POST.get("content")
        kwargs['title'] = request.POST.get("title")
        post_id = int(kwargs['pk'])
        kwargs.pop('pk')
        if request.POST.get("content") and request.POST.get("title"):
            category = [int(i) for i in request.POST.getlist("category") if i]
            Post.objects.filter(pk=post_id).update(**kwargs)
            post = Post.objects.get(pk=post_id)
            current_category = [i['pk'] for i in post.category.all().values("pk")]
            if current_category != category:
                post.category.clear()
                post.category.add(*category)
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            if not request.POST.get("title"):
                messages.add_message(self.request, messages.ERROR, _('title is required'))
            if not request.POST.get("content"):
                messages.add_message(self.request, messages.ERROR, _('content is required'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DiscussionDelete(DeleteView):

    model = Post
    success_url = reverse_lazy('personal_interface')
    template_name = 'comfirm_delete.html'

    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, *args, **kwargs):
        return super(DiscussionDelete, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DiscussionDelete, self).get_object()
        tzinfo = obj.created.tzinfo
        try:
            if obj.author != self.request.user or obj.created < datetime.datetime.now(
                    tz=tzinfo)-datetime.timedelta(days=1):
                raise Http404
        except ObjectDoesNotExist:
                raise Http404
        return obj


class CategoryCreate(CreateView):
    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, *args, **kwargs):
        return super(CategoryCreate, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        category, created = Category.objects.get_or_create(name=request.GET.get("category"))
        if created:
            data = serializers.serialize("json", [category, ])
            return HttpResponse(data, content_type='application/json')
        else:
            return HttpResponse(category.pk, status='400')


class CommentPost(FormView):
    model = Comments
    form_class = CommentsForm

    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, *args, **kwargs):
        return super(CommentPost, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        content = request.POST.get("content")
        comment_user = request.user
        comment_post = request.POST.get("post_id")
        if content:
            Comments.objects.create(content=content, post=Post.objects.get(pk=comment_post), user=comment_user)
            return HttpResponseRedirect("/discussion/detail/%s" % comment_post)
        else:
            messages.add_message(self.request, messages.ERROR, _('comment content is required'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CommentDelete(DeleteView):

    model = Comments
    success_url = reverse_lazy('personal_interface')
    template_name = 'comfirm_delete.html'

    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, *args, **kwargs):
        return super(CommentDelete, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(CommentDelete, self).get_object()
        tzinfo = obj.created.tzinfo
        try:
            if obj.user != self.request.user or obj.created < datetime.datetime.now(
                    tz=tzinfo)-datetime.timedelta(days=1):
                raise Http404
        except ObjectDoesNotExist:
                raise Http404
        return obj


class PersonalInterface(TemplateView):

    template_name = 'personal_interface.html'

    def get_context_data(self, **kwargs):
        context = super(PersonalInterface, self).get_context_data(**kwargs)
        context['discussions'] = Post.objects.filter(
            author=self.request.user).filter(created__gte=datetime.date.today()).order_by('-created')
        context['comments'] = Comments.objects.filter(
            user=self.request.user).filter(created__gte=datetime.date.today()).order_by('-created')
        return context


class PostSearchView(SearchView):
    """My custom search view."""
    template_name = 'search/discussion_search.html'
    paginate_by = 10

    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, *args, **kwargs):
        return super(PostSearchView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(PostSearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        # post_perm_list = [i for i in queryset.models(Post) if i.object.get_post_perm(self.request.user)]
        return queryset.models(Post)

    def get_context_data(self, *args, **kwargs):
        context = super(PostSearchView, self).get_context_data(**kwargs)
        context['object_list'] = [i for i in context['object_list'] if i]
        context['object_list'] = [i for i in context['object_list'] if i.object.get_post_perm(self.request.user)]
        return context
