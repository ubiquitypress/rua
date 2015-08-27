from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
	# Review
	url(r'^request/submission/(?P<submission_id>\d+)/returner/(?P<returner>[-\w]+)/$', 'revisions.views.request_revisions', name='request_revisions'),
	url(r'^(?P<revision_id>\d+)/$', 'revisions.views.revision', name='revision'),
	url(r'^(?P<revision_id>\d+)/file/(?P<file_id>\d+)/update/$', 'revisions.views.update_file', name='revision_update_file'),
)
