from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # New Submissions
    url(r'^new/$', 'workflow.views.new_submissions', name='new_submissions'),
    url(r'^new/(?P<submission_id>\d+)/$', 'workflow.views.view_new_submission', name='view_new_submission'),
    url(r'^submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/download/$', 'workflow.views.serve_file', name='serve_file'),

    url(r'^review/$', 'workflow.views.in_review', name='in_review'),
    url(r'^editing/$', 'workflow.views.in_editing', name='in_editing'),
    url(r'^production/$', 'workflow.views.in_production', name='in_production'),

    url(r'^log/(?P<submission_id>\d+)/', 'workflow.views.view_log', name='view_log'),

)