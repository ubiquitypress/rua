from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # New Submissions
    url(r'^$', 'manager.views.index', name='manager_index'),
    url(r'^groups/$', 'manager.views.groups', name='manager_groups'),
    url(r'^groups/order/$', 'manager.views.groups_order', name='manager_groups_order'),
    url(r'^groups/add/$', 'manager.views.group', name='manager_group_add'),
    url(r'^groups/(?P<group_id>\d+)/edit/$', 'manager.views.group', name='manager_group_edit'),
    url(r'^groups/(?P<group_id>\d+)/delete/$', 'manager.views.group_delete', name='manager_group_delete'),
    url(r'^groups/(?P<group_id>\d+)/members/$', 'manager.views.group_members', name='manager_group_members'),
    url(r'^groups/(?P<group_id>\d+)/members/user/(?P<user_id>\d+)/assign/$', 'manager.views.group_members_assign', name='group_members_assign'),
    url(r'^groups/(?P<group_id>\d+)/members/order$', 'manager.views.group_members_order', name='group_members_order'),
    url(r'^groups/(?P<group_id>\d+)/members/(?P<member_id>\d+)/delete$', 'manager.views.manager_membership_delete', name='manager_membership_delete'),
)
