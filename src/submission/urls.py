from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

	 url(r'^book/$', 'submission.views.start_submission', name='submission_start'),
	 url(r'^proposal/$', 'submission.views.start_proposal', name='proposal_start'),
)
