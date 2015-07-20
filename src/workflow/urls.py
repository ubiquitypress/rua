from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # Proposals
    url(r'^proposals/$', 'workflow.views.proposal', name='proposals'),
    url(r'^proposals/(?P<proposal_id>\d+)/$', 'workflow.views.view_proposal', name='view_proposal'),
    url(r'^proposals/(?P<proposal_id>\d+)/review/start/$', 'workflow.views.start_proposal_review', name='start_proposal_review'),
    url(r'^proposals/(?P<proposal_id>\d+)/review/add/$', 'workflow.views.add_proposal_reviewers', name='add_proposal_reviewers'),
    url(r'^proposals/(?P<submission_id>\d+)/assignment/(?P<assignment_id>\d+)/$', 'workflow.views.view_proposal_review', name='view_proposal_review'),
    url(r'^proposals/(?P<proposal_id>\d+)/accept/$', 'workflow.views.accept_proposal', name='accept_proposal'),
    url(r'^proposals/(?P<proposal_id>\d+)/revisions/$', 'workflow.views.request_proposal_revisions', name='request_proposal_revisions'),
    url(r'^proposals/(?P<proposal_id>\d+)/decline/$', 'workflow.views.decline_proposal', name='decline_proposal'),
    
    # New Submissions
    url(r'^new/$', 'workflow.views.new_submissions', name='new_submissions'),
    url(r'^new/(?P<submission_id>\d+)/$', 'workflow.views.view_new_submission', name='view_new_submission'),

    # Files
    url(r'^submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/download/$', 'workflow.views.serve_file', name='serve_file'),
    url(r'^submission/(?P<submission_id>\d+)/file/(?P<revision_id>\d+)/download_versioned_file/$', 'workflow.views.serve_versioned_file', name='serve_versioned_file'),
    url(r'^submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/delete/returner/(?P<returner>[-\w]+)/$', 'workflow.views.delete_file', name='delete_file'),
    url(r'^submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/update/returner/(?P<returner>[-\w]+)/$', 'workflow.views.update_file', name='update_file'),
    url(r'^submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/versions/$', 'workflow.views.versions_file', name='versions_file'),

    # Decline
    url(r'^submission/(?P<submission_id>\d+)/decline/$', 'workflow.views.decline_submission', name='decline_submission'),

    # Review
    url(r'^review/$', 'workflow.views.in_review', name='in_review'),
    url(r'^review/(?P<submission_id>\d+)/$', 'workflow.views.view_review', name='view_review'),
    url(r'^review/(?P<submission_id>\d+)/new_round/$', 'workflow.views.add_review_round', name='add_review_round'),
    url(r'^review/(?P<submission_id>\d+)/assignment/(?P<assignment_id>\d+)/$', 'workflow.views.view_review_assignment', name='view_review_assignment'),
    url(r'^review/(?P<submission_id>\d+)/files/(?P<review_type>[-\w]+)/add/$', 'workflow.views.add_review_files', name='add_review_files'),
    url(r'^review/(?P<submission_id>\d+)/files/(?P<file_id>\d+)/(?P<review_type>[-\w]+)/delete/$', 'workflow.views.delete_review_files', name='delete_review_files'),
    url(r'^review/(?P<submission_id>\d+)/reviewers/(?P<review_type>[-\w]+)/add/(?P<round_number>\d+)/$', 'workflow.views.add_reviewers', name='add_reviewers'),
    url(r'^review/move/(?P<submission_id>\d+)/editing/$', 'workflow.views.move_to_editing', name='move_to_editing'),

    # Editing
    url(r'^editing/$', 'workflow.views.in_editing', name='in_editing'),

    # Production
    url(r'^production/$', 'workflow.views.in_production', name='in_production'),
    url(r'^production/(?P<submission_id>\d+)/$', 'workflow.views.view_production', name='view_production'),
    url(r'^production/(?P<submission_id>\d+)/add/format/$', 'workflow.views.add_format', name='add_format'),
    url(r'^production/(?P<submission_id>\d+)/add/chapter/$', 'workflow.views.add_chapter', name='add_chapter'),
    url(r'^production/(?P<submission_id>\d+)/delete/(?P<format_or_chapter>[-\w]+)/(?P<id>\d+)/$', 'workflow.views.delete_format_or_chapter', name='delete_format_or_chapter'),
    url(r'^production/(?P<submission_id>\d+)/update/(?P<format_or_chapter>[-\w]+)/(?P<id>\d+)/$', 'workflow.views.update_format_or_chapter', name='update_format_or_chapter'),
    url(r'^production/(?P<submission_id>\d+)/catlog/$', 'workflow.views.catalog', name='catalog'),

    url(r'^log/(?P<submission_id>\d+)/', 'workflow.views.view_log', name='view_log'),

)
