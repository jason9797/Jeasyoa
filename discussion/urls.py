# -*- coding:utf-8 -*-
from django.conf.urls import url
from views import *

urlpatterns = [
               url(r'^list/$', DiscussionList.as_view(), name='discussion_list'),
               url(r'detail/(?P<pk>\d+)/$', DiscussionDetail.as_view(), name='discussion_detail'),
               url(r'update/(?P<pk>\d+)/$', DiscussionUpdate.as_view(), name='discussion_update'),
               url(r'delete/(?P<pk>\d+)/$', DiscussionDelete.as_view(), name='discussion_delete'),
               url(r'comments/$', CommentPost.as_view(), name='comment_post'),
               url(r'create/$', DiscussionCreate.as_view(), name='discussion_create'),
               url(r'comments/(?P<pk>\d+)/delete/$', CommentDelete.as_view(), name='comment_delete'),
               url(r'category/add/$', CategoryCreate.as_view(), name='category_create'),
               url(r'personal/interface/$', PersonalInterface.as_view(), name='personal_interface')
                ]
