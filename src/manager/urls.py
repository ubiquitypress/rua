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
)
