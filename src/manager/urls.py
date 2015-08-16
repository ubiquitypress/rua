from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # New Submissions
    url(r'^$', 'manager.views.index', name='manager_index'),

    # Group Management
    url(r'^groups/$', 'manager.views.groups', name='manager_groups'),
    url(r'^groups/order/$', 'manager.views.groups_order', name='manager_groups_order'),
    url(r'^groups/add/$', 'manager.views.group', name='manager_group_add'),
    url(r'^groups/(?P<group_id>\d+)/edit/$', 'manager.views.group', name='manager_group_edit'),
    url(r'^groups/(?P<group_id>\d+)/delete/$', 'manager.views.group_delete', name='manager_group_delete'),
    url(r'^groups/(?P<group_id>\d+)/members/$', 'manager.views.group_members', name='manager_group_members'),
    url(r'^groups/(?P<group_id>\d+)/members/user/(?P<user_id>\d+)/assign/$', 'manager.views.group_members_assign', name='group_members_assign'),
    url(r'^groups/(?P<group_id>\d+)/members/order$', 'manager.views.group_members_order', name='group_members_order'),
    url(r'^groups/(?P<group_id>\d+)/members/(?P<member_id>\d+)/delete$', 'manager.views.manager_membership_delete', name='manager_membership_delete'),

    # Role Management
    url(r'^roles/$', 'manager.views.roles', name='manager_roles'),
    url(r'^roles/(?P<slug>[-\w.]+)/$', 'manager.views.role', name='manager_role'),
    url(r'^roles/(?P<slug>[-\w.]+)/user/(?P<user_id>\d+)/(?P<action>[-\w.]+)/$', 'manager.views.role_action', name='manager_role_action'),

    # Settings Management
    url(r'^settings/$', 'manager.views.settings_index', name='settings_index'),
    url(r'^settings/group/(?P<setting_group>[-\w.]+)/setting/(?P<setting_name>[-\w.]+)/$', 'manager.views.edit_setting', name='edit_setting'),

    # Submission checklist
    url(r'^submission/checklist/$', 'manager.views.submission_checklist', name='submission_checklist'),
    url(r'^submission/proposal_forms/$', 'manager.views.proposal_forms', name='proposal_forms'),
    url(r'^submission/checklist/order/$', 'manager.views.checklist_order', name='checklist_order'),

    # Cache
    url(r'^cache/flush/$', 'manager.views.flush_cache', name='manager_flush_cache'),

)
