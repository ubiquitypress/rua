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
    url(r'^submission/checklist/edit/(?P<item_id>\d+)/$', 'manager.views.edit_submission_checklist', name='edit_submission_checklist'),
    url(r'^submission/checklist/delete/(?P<item_id>\d+)/$', 'manager.views.delete_submission_checklist', name='delete_submission_checklist'),
    url(r'^submission/checklist/order/$', 'manager.views.checklist_order', name='checklist_order'),
 
    #Proposal Form Management
    url(r'^submission/proposal_forms/$', 'manager.views.proposal_forms', name='proposal_forms'),
    url(r'^submission/proposal_forms/view/form/(?P<form_id>\d+)/$', 'manager.views.view_proposal_form', name='manager_view_proposal_form'),
    url(r'^submission/proposal_forms/form-elements/$', 'manager.views.proposal_form_elements', name='manager_proposal_form_elements'),
    #Form Creation
    url(r'^submission/proposal_forms/new/form/$', 'manager.views.add_proposal_form', name='manager_add_proposal_form'),
    url(r'^submission/proposal_forms/form/(?P<form_id>\d+)/create/elements/$', 'manager.views.create_proposal_elements', name='manager_create_proposal_elements'),
    url(r'^submission/proposal_forms/form/(?P<form_id>\d+)/edit/element/(?P<element_id>\d+)/$', 'manager.views.edit_proposal_element', name='manager_edit_proposal_element'),
    url(r'^submission/proposal_forms/form/(?P<form_id>\d+)/add/field/$', 'manager.views.add_proposal_field', name='manager_add_proposal_form_field'), 

    # Cache
    url(r'^cache/flush/$', 'manager.views.flush_cache', name='manager_flush_cache'),

    #Review Form Management
    url(r'^review-forms/$', 'manager.views.review_forms', name='manager_review_forms'),
    url(r'^review-forms/view/form/(?P<form_id>\d+)/$', 'manager.views.view_review_form', name='manager_view_review_form'),
    url(r'^review-forms/form-elements/$', 'manager.views.review_form_elements', name='manager_review_form_elements'),
    #Form Creation
    url(r'^review-forms/new/form/$', 'manager.views.add_form', name='manager_add_form'),
    url(r'^review-forms/form/(?P<form_id>\d+)/create/elements/$', 'manager.views.create_elements', name='manager_create_elements'),
    url(r'^review-forms/form/(?P<form_id>\d+)/add/field/$', 'manager.views.add_field', name='manager_add_review_form_field'),

    # Users
    url(r'^user/$', 'manager.views.users', name='manager_users'),
    url(r'^user/inactive/$', 'manager.views.inactive_users', name='manager_inactive_users'),
    url(r'^user/add/$', 'manager.views.add_user', name='add_user'),
    url(r'^user/(?P<user_id>\d+)/edit/$', 'manager.views.user_edit', name='user_edit'),

)
